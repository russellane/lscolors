"""Command line interface base module."""

import argparse
import contextlib
import functools
import importlib.metadata
import logging
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import Callable, Iterable, List, Optional

import argcomplete
import termui
import toml
import tomli


class BaseCLI:
    """Command line interface base class."""

    argv: [str] = []
    config: dict = {}
    exclude_print_config: [str] = []
    parser: argparse.ArgumentParser = None
    options: argparse.Namespace = None
    add_parser: Callable = None
    help_line_ending = "."

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
        argcomplete.autocomplete(self.parser)
        self.options = self._parse_args()

    def init_config(self) -> None:
        """Parse cmdline to load contents of `--config FILE` only.

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
        """Set stdlib logging level based on `--verbose`."""
        # pylint: disable=no-self-use; needed by super in subclasses.
        _ = [logging.WARNING, logging.INFO, logging.DEBUG]
        logging.basicConfig(level=_[min(verbose, len(_) - 1)])

    def init_parser(self) -> None:
        """Implement in subclass, if desired."""
        self.ArgumentParser()

    def set_defaults(self) -> None:
        """Implement in subclass, if desired."""

    def add_arguments(self) -> None:
        """Implement in subclass, probably desired."""

    def ArgumentParser(self, **kwargs) -> argparse.ArgumentParser:  # noqa:
        """Initialize argument parser.

        This wraps `argparse.ArgumentParser` to provide common features to all CLI's:

            * color formatter_class when interactive
            * -X:  hidden option for our internal use
            * --verbose option
            * --version option
            * --config-file option
            * --print-config option
        """

        if "formatter_class" not in kwargs:
            # wide terminals are great, but not for reading/printing manuals.
            width = min(97, termui.get_terminal_size()[0])
            formatter = PdmFormatter if os.isatty(1) else argparse.RawDescriptionHelpFormatter
            kwargs["formatter_class"] = lambda prog: formatter(
                prog, max_help_position=35, width=width
            )

        self.parser = argparse.ArgumentParser(**kwargs)
        self._add_common_options(self.parser)
        return self.parser

    def add_argument(self, *args, **kwargs) -> argparse.Action:
        """Wrap `add_argument` to conform help text line endings."""

        if "help" in kwargs:
            kwargs["help"] = self.format_help(kwargs["help"])
        return self.parser.add_argument(*args, **kwargs)

    def add_subcommand_classes(self, subcommand_classes) -> None:
        """Add list of subcommands to parser."""

        # https://docs.python.org/3/library/argparse.html#sub-commands

        self.init_subcommands(metavar="COMMAND", title="Specify one of")
        self.parser.set_defaults(cmd=None)
        for subcommand_class in subcommand_classes:
            subcommand_class(self)

        # equiv to module: .commands.help import Command as HelpCommand
        # sub = self.add_subcommand_parser("help", help="same as `--help`")
        # sub.set_defaults(cmd=self.parser.print_help)

    def init_subcommands(self, **kwargs):
        """Prepare to add subcommands to main parser."""

        subparsers = self.parser.add_subparsers(**kwargs)
        self.add_parser = subparsers.add_parser

    def add_default_to_help(self, arg: argparse.Action) -> None:
        """Show default value in help text."""

        default = self.parser.get_default(arg.dest)
        if isinstance(arg.const, bool) and not arg.const:
            default = not default
        arg.help += f" (default: `{default}`)"

    @staticmethod
    def dedent(text: str) -> str:
        """Make `textwrap.dedent` convenient."""
        return textwrap.dedent(text)

    # public
    # -------------------------------------------------------------------------------
    # private

    def _update_config_from_file(self) -> None:

        # sneak a peak for `--verbose` and `--config FILE`.
        parser = argparse.ArgumentParser(add_help=False)
        self._add_verbose_option(parser)
        self._add_config_option(parser)
        options, _ = parser.parse_known_args(self.argv)

        self.init_logging(options.verbose)

        if not options.config_file:
            logging.info("config-file not defined or given.")
            return

        logging.info("Reading config-file `%s`.", options.config_file)

        try:
            config = tomli.loads(options.config_file.read_text())
        except FileNotFoundError as err:
            if options.config_file != self.config["config-file"]:
                # postpone calling `parser.error` to full parser.
                self.config["config-file"] = err
            else:
                logging.info("%s; ignoring.", err)
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

        parser.add_argument(
            "-X",
            action="store_true",
            help=argparse.SUPPRESS,
        )

        self._add_verbose_option(self.parser)
        self._add_version_option(self.parser)

        if self.config.get("config-file"):
            self._add_config_option(self.parser)

        self.parser.add_argument(
            "--print-config",
            action="store_true",
            help=self.format_help("print effective configuration and exit"),
        )

    def _add_verbose_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--verbose` to given `parser`."""

        parser.add_argument(
            "-v",
            "--verbose",
            default=0,
            action="count",
            help=self.format_help("`-v` for detailed output and `-vv` for more detailed"),
        )

    def _add_version_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--version` to given `parser`."""

        version = "0.0.0"
        with contextlib.suppress(importlib.metadata.PackageNotFoundError):
            version = importlib.metadata.version(__package__)

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=version,
            help=self.format_help("print version number and exit"),
        )

    def _add_config_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--config FILE` to given `parser`."""

        text = "configuration file"
        if file := self.config.get("config-file"):
            text += f" (default: `{file}`)"

        parser.add_argument(
            "--config",
            dest="config_file",
            metavar="FILE",
            default=file,
            type=Path,
            help=self.format_help(text),
        )

    def _parse_args(self) -> argparse.Namespace:
        """Parse command line and return options."""

        options = self.parser.parse_args(self.argv)

        if isinstance(self.config.get("config-file"), Exception):
            # postponed from load_config
            self.parser.error(self.config["config-file"])

        self._update_config_from_options(options)

        if hasattr(options, "print_config") and options.print_config:
            self._print_config(options)
            sys.exit(0)

        if hasattr(options, "X") and options.X:
            print(self.__dict__)
            print(self.options)
            sys.exit(0)

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
        print(toml.dumps(config))

    def format_help(self, text: str) -> str:
        """Conform help text line-endings."""
        if text and self.help_line_ending and not text.endswith(self.help_line_ending):
            return text + self.help_line_ending
        return text


yellow = functools.partial(termui.style, fg="yellow")
cyan = functools.partial(termui.style, fg="cyan")


class PdmFormatter(argparse.RawDescriptionHelpFormatter):
    """Colorize help."""

    def start_section(self, heading: str) -> None:
        """Colorize start of help section."""

        return super().start_section(yellow(heading.title() if heading else heading, bold=True))

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

    def _format_text(self, text):
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
