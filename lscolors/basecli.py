"""Command line interface base module."""

import argparse
import contextlib
import functools
import importlib
import importlib.metadata
import logging
import pkgutil
import re
import sys
import textwrap
from pathlib import Path
from pprint import pformat
from typing import Callable, Iterable, List, Optional

import argcomplete
import termui
import tomli

with contextlib.suppress(ImportError):
    from loguru import logger  # noqa

with contextlib.suppress(ImportError):
    import icecream  # noqa
    from icecream import ic  # noqa

    icecream.install()
    icecream.ic.configureOutput(prefix="=====>\n", includeContext=True)

# pylint: disable=protected-access


class BaseHelpAction(argparse._HelpAction):
    # pylint: disable=too-few-public-methods
    """Base class for our help actions."""


class BaseCLI:
    """Command line interface base class."""

    argv: [str] = []
    config: dict = {}
    exclude_print_config: [str] = []
    parser: argparse.ArgumentParser = None
    options: argparse.Namespace = None
    add_parser: Callable = None
    help_first_char = "upper"
    help_line_ending = "."
    init_logging_called = False

    def __init__(self, argv: Optional[List[str]] = None) -> None:
        """Build and parse command line.

        Args:
            argv:       command line argument list.

        Attributes:
            argv:       command line argument list of strings.
            config:     configuration dict.
            exclude_print_config: list of keys to not write to config-file.
            parser:     argument parser.
            options:    parsed arguments; from `self.parser.parse_args(argv)`.
        """

        self.argv = argv
        self.init_config()
        self.init_parser()
        self.set_defaults()
        self.add_arguments()
        self._add_common_options(self.parser)
        self._finalize()
        argcomplete.autocomplete(self.parser)
        self.options = self._parse_args()

    def init_config(self) -> None:
        """Parse command line to load contents of `--config FILE` only.

        Reads `--config FILE` if given, else `self.config["config-file"]`
        if present, making the effective configuration available to
        building the ArgumentParser, add_argument, set_defaults, etc.
        """

        base_config = {
            # name of config file
            # optional: adds `--config FILE` option when set.
            # regardless: `--print-config` will be added.
            "config-file": None,
            # toml [section-name]
            # optional:
            # encouraged:
            # regardless: of `config-file`.
            "config-name": None,
            # --verbose
            "verbose": 0,
        }

        # merge any missing base items into user items.
        if self.config:
            base_config.update(self.config)
        self.config = base_config

        # don't `--print-config` any of the base items or user excludes.
        for key in base_config:
            if key not in self.exclude_print_config:
                self.exclude_print_config.append(key)

        self._update_config_from_file()

    def init_logging(self, verbose: int) -> None:
        """Set logging levels based on `--verbose`."""

        if not self.init_logging_called:
            self.__class__.init_logging_called = True

            # stdlib:
            #    (dflt)           -v            -vv
            _ = [logging.WARNING, logging.INFO, logging.DEBUG]
            logging.basicConfig(level=_[min(verbose, len(_) - 1)])

            if "logger" in globals():
                # loguru:
                #    (dflt)  -v       -vv
                _ = ["INFO", "DEBUG", "TRACE"]
                level = _[min(verbose, len(_) - 1)]
                logger.remove()
                logger.add(sys.stderr, level=level)

    def init_parser(self) -> None:
        """Implement in subclass, if desired."""
        self.ArgumentParser()

    def set_defaults(self) -> None:
        """Implement in subclass, if desired."""

    def add_arguments(self) -> None:
        """Implement in subclass, probably desired."""

    def ArgumentParser(self, **kwargs) -> argparse.ArgumentParser:  # noqa: snake-case
        """Initialize `self.parser`."""

        kwargs["add_help"] = False
        self.parser = argparse.ArgumentParser(**kwargs)
        self.parser.set_defaults(cli=self)
        return self.parser

    # def add_argument(self, *args, **kwargs) -> argparse.Action:
    #     """Wrap `add_argument` for no good reason anymore."""
    #     return self.parser.add_argument(*args, **kwargs)

    def add_subcommand_classes(self, subcommand_classes) -> None:
        """Add list of subcommands to this parser."""

        # https://docs.python.org/3/library/argparse.html#sub-commands
        self.init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)
        for subcommand_class in subcommand_classes:
            subcommand_class(self)

        # equiv to module: .commands.help import Command as HelpCommand
        # sub = self.add_subcommand_parser("help", help="same as `--help`")
        # sub.set_defaults(cmd=self.parser.print_help)

    def add_subcommand_modules(
        self,
        modname: str,
        prefix: str = None,
        suffix: str = None,
    ) -> None:
        """Add all subcommands in module `modname`.

        e.g., cli.add_subcommand_modules("wumpus.commands")
        or,   cli.add_subcommand_modules("wumpus.cli.commands")
        or wherever your command modules are.

        1. Load each module in containing module `modname`,
        2. Instantiate an instance each module's `Command` class, and
        3. Add the command to this cli.

        If all command classes are not named `Command`, then they must all
        begin and/or end with common tags. Pass `prefix` and/or `suffix` to
        specify, and the longest matching class will be used. Multiple
        command classes could be defined in one module this way.

        e.g.,
            wumpus/commands/left.py
                class WumpusLeftCmd(BaseCmd):
                    ...

            wumpus/commands/right.py
                class WumpusCmd(BaseCmd):
                    ...
                class WumpusRightCmd(WumpusCmd)
                    ...

            cli.add_subcommand_modules("wumpus.commands", prefix="Wumpus", suffix="Cmd")
        """

        self.init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)

        commands_module_path = importlib.import_module(modname, __name__).__path__
        base_name = prefix + suffix

        for modinfo in pkgutil.iter_modules(commands_module_path):
            module = importlib.import_module(f"{modname}.{modinfo.name}", __name__)

            if prefix is None and suffix is None:
                try:
                    cmd_class = module.Command
                except AttributeError:
                    continue
                cmd_class(self)
                continue

            for name in [x for x in dir(module) if x != base_name]:
                if prefix and not name.startswith(prefix):
                    continue
                if suffix and not name.endswith(suffix):
                    continue
                try:
                    cmd_class = getattr(module, name)
                except AttributeError:
                    continue
                cmd_class(self)

    def init_subcommands(self, **kwargs):
        """Prepare to add subcommands to main parser."""

        subparsers = self.parser.add_subparsers(**kwargs)
        self.add_parser = subparsers.add_parser

    def add_default_to_help(
        self,
        arg: argparse.Action,
        parser: argparse.ArgumentParser = None,
    ) -> None:
        """Add default value to help text for `arg` in `parser`."""

        if parser is None:
            parser = self.parser
        default = parser.get_default(arg.dest)
        if default is None:
            return
        if isinstance(arg.const, bool) and not arg.const:
            default = not default
        else:
            default = str(default)
            home = str(Path.home())
            if default.startswith(home):
                default = "~" + default[len(home) :]
        default = f" (default: `{default}`)"

        if arg.help.endswith(self.help_line_ending):
            arg.help = arg.help[: -len(self.help_line_ending)] + default + self.help_line_ending
        else:
            arg.help += default

    def normalize_help_text(self, text: str) -> str:
        """Return help `text` with normalized first-character and line-ending."""

        if text and text != argparse.SUPPRESS:
            if self.help_line_ending and not text.endswith(self.help_line_ending):
                text += self.help_line_ending
            if self.help_first_char == "upper":
                text = text[0].upper() + text[1:]
            elif self.help_first_char == "lower":
                text = text[0].lower() + text[1:]
        return text

    @staticmethod
    def dedent(text: str) -> str:
        """Make `textwrap.dedent` convenient."""
        return textwrap.dedent(text).strip()

    def error(self, text: str) -> None:
        """Print an ERROR message to `stdout`."""
        _ = self  # unused; avoiding @staticmethod
        termui.secho("ERROR: " + text, fg="red")

    def info(self, text: str) -> None:
        """Print an INFO message to `stdout`."""
        if self.options.verbose > 0:
            termui.secho("INFO: " + text, fg="cyan")

    def debug(self, text: str) -> None:
        """Print a DEBUG message to `stdout`."""
        if self.options.verbose > 1:
            termui.secho("DEBUG: " + text, fg="white")

    # public
    # -------------------------------------------------------------------------------
    # private

    def _update_config_from_file(self) -> None:

        # sneak a peak for `--verbose` and `--config FILE`.
        parser = argparse.ArgumentParser(add_help=False)
        self._add_verbose_option(parser)
        self._add_config_option(parser)
        self.options, _ = parser.parse_known_args(self.argv)

        self.init_logging(self.options.verbose)

        if not self.options.config_file:
            self.debug("config-file not defined or given.")
            return

        self.debug(f"reading config-file `{self.options.config_file}`.")

        try:
            config = tomli.loads(self.options.config_file.read_text())
        except FileNotFoundError as err:
            if self.options.config_file != self.config["config-file"]:
                # postpone calling `parser.error` to full parser.
                self.config["config-file"] = err
            else:
                self.debug(f"{err}; ignoring.")
            return

        if (section := self.config.get("config-name")) is not None:
            config = config.get(section, config)

        for name, value in config.items():
            if name in self.config:
                _type = type(self.config[name])
                config[name] = _type(value)

        self.config.update(config)

    def _add_common_options(self, parser: argparse.ArgumentParser) -> None:
        """Add common options to given `parser`."""

        group = parser.add_argument_group("General options")

        group.add_argument(
            "-X",
            action=DebugAction,
            help=argparse.SUPPRESS,
        )

        group.add_argument(
            "-h",
            "--help",
            action=BaseHelpAction,
            help="show this help message and exit",
        )

        if self.add_parser:
            group.add_argument(
                "-H",
                "--long-help",
                action=LongHelpAction,
                help="show help for all commands and exit",
            )

        # Only really needs to be added when `not self.add_parser`;
        # adding regardless, for muscle-memoried developers at the cli.
        group.add_argument(
            "--md-help",
            action=MarkdownHelpAction,
            help=argparse.SUPPRESS,
            # help="show this help message in markdown format and exit",
        )

        self._add_verbose_option(group)
        self._add_version_option(group)

        if self.config.get("config-file"):
            self._add_config_option(group)

        group.add_argument(
            "--print-config",
            action=PrintConfigAction,
            help="print effective config and exit",
        )

        group.add_argument(
            "--print-url",
            action=PrintUrlAction,
            help="print project url and exit",
        )

    @staticmethod
    def _add_verbose_option(parser: argparse.ArgumentParser) -> None:
        """Add `--verbose` to given `parser`."""

        parser.add_argument(
            "-v",
            "--verbose",
            default=0,
            action="count",
            help="`-v` for detailed output and `-vv` for more detailed",
        )

    @staticmethod
    def _add_version_option(parser: argparse.ArgumentParser) -> None:
        """Add `--version` to given `parser`."""

        version = "0.0.0"
        with contextlib.suppress(importlib.metadata.PackageNotFoundError):
            # https://docs.python.org/3/library/importlib.metadata.html#distribution-versions
            version = importlib.metadata.version(__package__)

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=version,
            help="print version number and exit",
        )

    def _add_config_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--config FILE` to given `parser`."""

        arg = parser.add_argument(
            "--config",
            dest="config_file",
            metavar="FILE",
            default=self.config.get("config-file"),
            type=Path,
            help="use config `FILE`",
        )
        self.add_default_to_help(arg, parser)

    def _finalize(self) -> None:
        """Normalize `formatter_class` and `help` text of all parsers."""

        # wide terminals are great, but not for reading/printing manuals.
        width = min(97, termui.get_terminal_size()[0])
        if sys.stdout.isatty():
            formatter = ColorHelpFormatter
        else:
            formatter = argparse.RawDescriptionHelpFormatter
        formatter_class = lambda prog: formatter(prog, max_help_position=35, width=width)  # noqa

        if self.parser.formatter_class == argparse.HelpFormatter:
            self.parser.formatter_class = formatter_class

        for action in self.parser._actions:
            if isinstance(action, argparse._SubParsersAction):
                for choice in action._choices_actions:
                    choice.help = self.normalize_help_text(choice.help)
                for subparser in action.choices.values():
                    if subparser.formatter_class == argparse.HelpFormatter:
                        subparser.formatter_class = formatter_class
                    if subparser._actions:
                        for subact in subparser._actions:
                            subact.help = self.normalize_help_text(subact.help)
            else:
                action.help = self.normalize_help_text(action.help)

    def _parse_args(self) -> argparse.Namespace:
        """Parse command line and return options."""

        options = self.parser.parse_args(self.argv)

        if isinstance(self.config.get("config-file"), Exception):
            # postponed from load_config
            self.parser.error(self.config["config-file"])

        self._update_config_from_options(options)
        return options

    def _update_config_from_options(self, options):

        for name, value in self.config.items():
            if name not in self.exclude_print_config:
                optname = name.replace("-", "_")
                self.config[name] = getattr(options, optname, value)

    def _print_config(self, options):

        config = {}
        for name, value in self.config.items():
            if name not in self.exclude_print_config:
                optname = name.replace("-", "_")
                value = getattr(options, optname, value)
                config[name] = value if isinstance(value, (int, str)) else str(value)

        if (name := self.config.get("config-name")) is not None:
            config = {name: config}
        print(pformat(config))

    @staticmethod
    def _print_url() -> None:

        # https://packaging.python.org/en/latest/specifications/core-metadata/#project-url-multiple-use
        distro = importlib.metadata.distribution(__package__)
        project_url = distro.metadata.get("Project-URL")
        print(project_url)


class DebugAction(BaseHelpAction):
    """Print internal data structures."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print internal data structures."""

        if "ic" in globals():
            ic(namespace.cli.__dict__)
            ic(parser.__dict__)
            ic(namespace)
        else:
            print(pformat(namespace.cli.__dict__))
            print(pformat(parser.__dict__))
            print(pformat(namespace))
        parser.exit()


class PrintConfigAction(BaseHelpAction):
    """Print effective config and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print effective config and exit."""

        namespace.cli._print_config(namespace)
        parser.exit()


class PrintUrlAction(BaseHelpAction):
    """Print project url and exit."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print project url and exit."""

        namespace.cli._print_url()
        parser.exit()


class LongHelpAction(BaseHelpAction):
    """Print help for all commands in color or markdown."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Print help for all commands in color or markdown."""

        def _print_help(atx: str, parser) -> None:
            if sys.stdout.isatty():
                print(f" {parser.prog.upper()} ".center(80, "-") + "\n")
                print(parser.format_help())
            else:
                print(atx, parser.prog)
                print("```\n" + parser.format_help().rstrip() + "\n```\n")

        _print_help("#", parser)

        for action in parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for subparser in action.choices.values():
                    _print_help("##", subparser)

        parser.exit()


#   @staticmethod
#   def _see_also(parser) -> str:
#
#       # xylint: disable=protected-access
#       also = {}
#       for action in parser._subparsers._actions:
#           if isinstance(action, argparse._SubParsersAction):
#               for name in action.choices:
#                   also[name] = f"{parser.prog}-{name}"
#       if not also:
#           return ""
#
#       formatter = parser._get_formatter()
#       return "\n\nSee Also: \n" + textwrap.fill(
#           ", ".join(also.values()) + ".",
#           width=formatter._width,
#           initial_indent=" " * formatter._indent_increment,
#           subsequent_indent=" " * formatter._indent_increment,
#       )

# -------------------------------------------------------------------------------


class BaseCmd:
    """Base command class."""

    def __init__(self, cli: BaseCLI) -> None:
        """Initialize base command instance."""

        self.cli = cli
        self.add_parser = self.cli.add_parser
        self.options: argparse.Namespace = None
        self.init_command()

    def init_command(self):
        """Implement in subclass to call `add_parser` and `add_argument`."""
        # raise NotImplementedError

    def add_subcommand_parser(self, name, **kwargs) -> argparse._SubParsersAction:
        """Add subcommand to main parser and return subcommand's subparser.

        Wrap `ArgumentParser.add_subparsers.add_parser`.
        """

        parser = self.cli.add_parser(name, **kwargs)
        parser.set_defaults(cmd=lambda: self._promote_options(self.run), prog=name)
        return parser

    def _promote_options(self, run):
        self.options = self.cli.options
        run()

    def run(self) -> None:
        """Perform the command."""
        # raise NotImplementedError


yellow = functools.partial(termui.style, fg="yellow")
cyan = functools.partial(termui.style, fg="cyan")


class ColorHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Colorize help."""

    def start_section(self, heading: str) -> None:
        """Colorize start of help section."""

        return super().start_section(yellow(heading.title() if heading else heading, bold=True))

    def add_text(self, text):
        """Colorize and add `text` to section."""
        if text:
            text = re.sub(r"`([^`]*)`", yellow(r"`\1`"), text)
        super().add_text(text)

    def _format_usage(
        self,
        usage: str,
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._ArgumentGroup],
        prefix: str,
    ) -> str:
        if prefix is None:
            prefix = "Usage: "
        result = super()._format_usage(usage, actions, groups, prefix)
        if prefix:
            return result.replace(prefix, yellow(prefix, bold=True))
        return result

    def _format_text(self, text: str) -> str:
        text = super()._format_text(text)
        text = re.sub(r"`([^`]*)`", yellow(r"`\1`"), text)
        return text

    def _format_action(self, action: argparse.Action) -> str:
        # determine the required width and the entry label
        help_position = min(self._action_max_length + 2, self._max_help_position)
        help_width = max(self._width - help_position, 11)
        action_width = help_position - self._current_indent - 2
        action_header = self._format_action_invocation(action)

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup  # noqa: f-string

        # short action name; start on the same line and pad two spaces
        elif len(action_header) <= action_width:
            tup = self._current_indent, "", action_width, action_header  # type: ignore
            action_header = "%*s%-*s  " % tup  # type: ignore  # noqa: f-string
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, "", action_header  # type: ignore
            action_header = "%*s%s\n" % tup  # noqa: f-string
            indent_first = help_position

        # collect the pieces of the action help
        parts = [cyan(action_header)]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            help_text = re.sub(r"`([^`]*)`", yellow(r"`\1`"), help_text)
            help_lines = self._split_lines(help_text, help_width)
            parts.append("%*s%s\n" % (indent_first, "", help_lines[0]))  # noqa: f-string
            for line in help_lines[1:]:
                parts.append("%*s%s\n" % (help_position, "", line))  # noqa: f-string

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith("\n"):
            parts.append("\n")

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)


class MarkdownHelpAction(BaseHelpAction):
    """Docstring."""

    def __call__(self, parser, namespace, values, option_string=None):
        """Docstring."""

        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()


class MarkdownHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Render help in `markdown` format."""

    # pylint: disable=consider-using-f-string

    @classmethod
    def _md_code(cls, raw_text, language=None):
        return (
            f"```{language or ''}\n"
            + cls._md_escape(raw_text.rstrip(), characters="`")
            + "\n```\n\n"
        )

    @staticmethod
    def _md_escape(raw_text, characters="*_"):
        def _escape_char(match):
            return "\\%s" % match.group(0)

        pattern = "[%s]" % re.escape(characters)
        return re.sub(pattern, _escape_char, raw_text)

    @staticmethod
    def _md_heading(raw_text, level):
        adjusted_level = min(max(level, 0), 6)
        return "%s%s%s" % ("#" * adjusted_level, " " if adjusted_level > 0 else "", raw_text)

    # def md_inline_code(raw_text):
    #     return "`%s`" % _md_escape(raw_text, characters="`")
    #
    # def md_bold(raw_text):
    #     return "**%s**" % _md_escape(raw_text, characters="*")
    #
    # def md_italic(raw_text):
    #     return "*%s*" % _md_escape(raw_text, characters="*")
    #
    # def md_link(link_text, link_target):
    #     return "[%s](%s)" % (
    #         _md_escape(link_text, characters="]"),
    #         _md_escape(link_target, characters=")"),
    #     )

    def __init__(
        self,
        prog,
        indent_increment=2,
        max_help_position=24,
        width=None,
    ):
        """Initialize MarkdownHelpFormatter."""
        max_help_position = 35
        width = 97
        self._md_level = {
            "title": 3,  # 1 and 2 render <hr/> on github
            "heading": 4,
        }

        super().__init__(prog, indent_increment, max_help_position, width)

        self._md_title = self._prog
        path = Path("pyproject.toml")
        if (
            path.exists()
            and (config := tomli.loads(path.read_text(encoding="utf-8")))
            and (project := config.get("project"))
            and (description := project.get("description"))
        ):
            self._md_title += " - " + description

    def _format_usage(self, usage, actions, groups, prefix):

        usage_text = super()._format_usage(usage, actions, groups, prefix)

        str_usage = "usage: "
        if not usage_text.startswith(str_usage):
            return self._md_code(usage_text)

        # Replace 1st len("usage: ") chars with 4 spaces on all lines.
        lines = usage_text.splitlines(keepends=True)
        lines = ["    " + x[len(str_usage) :] for x in lines]
        return (
            "\n"
            + self._md_heading("Usage", level=self._md_level["heading"])
            + "\n"
            + "".join(lines)
            + "\n"
        )

    def format_help(self):
        """Format help."""
        self._root_section.heading = self._md_heading(
            self._md_title, level=self._md_level["title"]
        )
        return super().format_help()

    def start_section(self, heading):
        """Start section."""
        if heading.startswith("options") or heading.startswith("positional arguments"):
            heading = heading.title()
        super().start_section(self._md_heading(heading, level=self._md_level["heading"]))

    def _format_action(self, action: argparse.Action) -> str:
        # indent at least 4 for code block
        _save_indent = self._current_indent
        self._current_indent = max(4, min(4, self._current_indent))
        action_help = super()._format_action(action)
        self._current_indent = _save_indent
        return action_help

    class _Section(argparse.HelpFormatter._Section):
        # pylint: disable=too-few-public-methods
        def format_help(self) -> str:
            # remove trailing colon from header line
            section_text = super().format_help()
            section_text = re.sub(r"^(\s*#+ [^\n]+):\n", "\\1\n", section_text)
            return section_text
