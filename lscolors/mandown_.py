"""MakedownHelpFormatter."""

import argparse
import pathlib
import re

import mandown.mandown

# -------------------------------------------------------------------------------
# /usr/lib/python3.8/argparse.py


class MarkdownHelpFormatter(argparse.HelpFormatter):
    """Docstring."""

    # def __init__(self, prog, indent_increment=2, max_help_position=24, width=None):
    def __init__(self, *args, **kwargs):
        """Docstring."""
        kwargs["width"] = 89
        super().__init__(*args, **kwargs)
        self._is_new_section = None
        self._have_epilog = False
        self._debug = False

    def _get_default_metavar_for_optional(self, action):
        return "=>" + action.dest.upper() + "<="

    def _get_default_metavar_for_positional(self, action):
        return "==>" + action.dest + "<=="

    def add_argument(self, action):
        """Override."""
        # pylint: disable=protected-access
        if isinstance(action, argparse._SubParsersAction):
            if self._debug:
                print("ADD_ARGUMENT: action=_SubParsersAction", flush=True)
        else:
            if self._debug:
                print(f"ADD_ARGUMENT: action={action}", flush=True)
        return super().add_argument(action)

    def _add_item(self, func, args):
        # breakpoint()
        if isinstance(args, tuple):
            action = args[1]  # line 265: args = usage, actions, groups, prefix
            # pylint: disable=protected-access
            if isinstance(action, argparse._SubParsersAction):
                if self._debug:
                    print("_ADD_ITEM: args.action=_SubParsersAction", flush=True)
            else:
                if self._debug:
                    print(f"_ADD_ITEM {action}", flush=True)
        super()._add_item(func, args)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = action.metavar
        elif action.choices is not None:
            choice_strs = [str(choice) for choice in action.choices]
            # pylint: disable=consider-using-f-string
            result = "{%s}" % ",".join(choice_strs)
        else:
            result = default_metavar

        result = f'<span style="color: darkred">***{result}***</span>'

        # pylint: disable=redefined-builtin
        def format(tuple_size):
            # pylint: disable=no-else-return
            if isinstance(result, tuple):
                return result
            else:
                return (result,) * tuple_size

        return format

    def _format_usage(self, usage, actions, groups, prefix):
        if self._debug:
            print(f"_FORMAT_USAGE: type(self)={type(self)}", flush=True)
            print(f"_FORMAT_USAGE: usage={usage}", flush=True)
            print(f"_FORMAT_USAGE: actions={actions}", flush=True)
            print(f"_FORMAT_USAGE: groups={groups}", flush=True)
            print(f"_FORMAT_USAGE: prefix={prefix}", flush=True)
        ret = super()._format_usage(usage, actions, groups, prefix)
        if self._debug:
            print(f"_FORMAT_USAGE: ret={ret}", flush=True)
        return ret

    #   def format_help(self):
    #       """Docstring."""
    #       print(f"FORMAT_HELP: type(self)={type(self)}", flush=True)
    #       # print(self._prog)
    #       # self._root_section.heading = '# Options: %s' % self._prog
    #       return super().format_help()

    def start_section(self, heading):
        """Docstring."""

        # print(f"START SECTION {heading!r}")
        super().start_section(f"### {heading}")
        self._is_new_section = True

    # def end_section(self):
    #     """Docstring."""
    #     # print("END SECTION")
    #     super().end_section()

    def add_text(self, text):
        """Docstring."""

        if (
            self._current_section == self._root_section
            and self._is_new_section is not None
            and not self._have_epilog
        ):
            self._have_epilog = True
            super().add_text("### Epilog")

        super().add_text(text)

    # -------------------------------------------------------------------------------

    def _format_action(self, action):
        # print(f"_FORMAT_ACTION: action.dest={action.dest}", flush=True)

        if action.dest == "command":
            return self._format_command_action(action)

        # print(f"action.default={action.default}", flush=True)
        if action.dest == "version":  # noqa: SIM114 Use logical or
            # version, new in 3.8, is suppressed by default.
            action.default = None

        elif action.dest == "help":
            # fix this - should not be necessary and incorrectly displays
            # what may have been intentionally hidden.
            action.default = None

        elif action.default == argparse.SUPPRESS:
            # print(f"suppressing {action.dest}", flush=True)
            return ""

        invocation = self._format_action_invocation(action)
        help_text = self._expand_help(action) if action.help else ""

        if self._is_new_section:
            self._is_new_section = False
            lines = [
                "| option | description |",
                "|:------ |:----------- |",
            ]
        else:
            lines = []

        # lines.append(f"| **{invocation}** | {help_text} |")
        lines.append(f"| {invocation} | {help_text} |")
        return "\n".join(lines) + "\n"

    # -------------------------------------------------------------------------------

    @staticmethod
    def _format_command_action(action):
        """New method."""

        lines = []

        for name, parser in action.choices.items():
            if (description := parser.description) is None:
                # print(f"Skipping={parser!r}")
                continue
            # print(f"\n=>name={name!r} parser={parser!r} description={description!r}")
            description = re.sub(" +", " ", description.replace("\n", " "))
            # print(parser.format_help())
            # print(f"\n=>name={name!r} parser={parser!r}")
            # breakpoint()
            # print(f"| [{name}](docs/{name}.md) | {description} |")
            lines.append(f"| [{name}](docs/{name}.md) | {description} |")

        if len(lines) == 0:
            return ""

        command = '<span style="color: darkred">***COMMAND***</span>'
        return (
            "\n".join(
                [
                    f"| {command} | |",
                    "|:--- | --- |",
                ]
                + lines
            )
            + "\n\n"
        )


# -------------------------------------------------------------------------------


def print_main_page(main_parser):
    """Print main help page."""

    save = main_parser.formatter_class
    main_parser.formatter_class = MarkdownHelpFormatter
    print(main_parser.format_help())
    main_parser.formatter_class = save


# -------------------------------------------------------------------------------


def write_command_pages(main_parser, directory):
    """Create separate pages for each command in `directory`."""

    also = _see_also(main_parser)

    # pylint: disable=protected-access
    for action in main_parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, parser in action.choices.items():
                lines = parser.format_help().splitlines()
                see_also = ", ".join([v for k, v in also.items() if k != name]) + "."
                mdoc = mandown.mandown.Mandown(lines, name=f"lscolors-{name}", see_also=see_also)
                text = mdoc.render_markdown()
                pathlib.Path(directory, name + ".md").write_text(text, encoding="utf-8")


# -------------------------------------------------------------------------------


def _see_also(main_parser):
    """Docstring."""

    also = {}

    # pylint: disable=protected-access
    for action in main_parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name in action.choices:
                also[name] = f"[lscolors-{name}]({name}.md)"

    return also


# -------------------------------------------------------------------------------
# class MarkdownHelpAction(argparse.Action):
#     """MD help action"""
#
#     def __init__(
#         self, option_strings, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, **kwargs
#     ):
#         super().__init__(
#             option_strings=option_strings, dest=dest, default=default, nargs=0, **kwargs
#         )
#
#     def __call__(self, parser, namespace, values, option_string=None):
#         parser.formatter_class = MarkdownHelpFormatter
#         parser.print_help()
#         parser.exit()
