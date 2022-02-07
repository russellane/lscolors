"""Create documentation for Subcommands."""

import pathlib

import argparse_color as argparse
import icecream
from argparse_color.coloring import Colors as _color
from icecream import ic

from lscolors.external.subcommands import command

from . import mkdir

icecream.install()
ic.configureOutput(prefix="\nic ===> ", includeContext=True)


class Command(command.Command):
    """Create documentation for Subcommands."""

    def __init__(self):
        """Initialize create documentation for Subcommands."""

        super().__init__()
        ic(self.__dict__)
        ic(self.parent.__dict__)
        parser = self.add_parser(
            "docs",
            help="Create documentation." if self.parent.show_docs else argparse.SUPPRESS,
            description="Create documentation files for this application.",
            epilog="This is an internal command used during the packaging process.",
        )

        parser.set_defaults(
            cmd=self.handle,
            docs="./docs",
        )

        # delete this - only here for debugging choices in argparse_color
        parser.add_argument(
            "format",
            nargs="?",
            choices=["ansi", "md", "txt"],
            help="Output format",
        )

        parser.add_argument(
            "docs",
            metavar="DIR",
            help="create directory `DIR`. " f"(default: {parser.get_default('docs')!r})",
        )

        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Ok to clobber `DIR` if it exists",
        )

    def handle(self, args):
        """Handle command invocation."""

        mkdir.mkdir(args.docs, args.force)
        self.print_main_page()
        self.write_command_pages(args.docs)

    def print_main_page(self):
        """Print main help page to `stdout`."""

        print(self.main_parser.format_help())

    def write_command_pages(self, directory):
        """Create separate help pages for each command in `directory`."""

        # pylint: disable=protected-access

        for action in self.main_parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, parser in action.choices.items():
                    helptext = parser.format_help() + self._see_also(parser)
                    pathlib.Path(directory, name + ".txt").write_text(helptext, encoding="utf-8")

    def _see_also(self, parser):
        """Return string with refs to other pages."""

        # pylint: disable=protected-access

        also = {}
        for action in self.main_parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, choice in action.choices.items():
                    if choice != parser:
                        also[name] = name
        if not also:
            return ""

        names = list(also.values())
        names[0] = f"{self.main_parser.prog} {names[0]}"
        text = ", ".join([f"`{x}`" for x in names]) + "."

        formatter = parser._get_formatter()
        formatter._indent()
        formatted = formatter._format_text(text)
        formatter._dedent()

        return f"\n{_color.section('See Also:')}\n{formatted}\n"


#       return (
#           "\n\nSee Also: \n"
#           + textwrap.fill(
#               ", ".join(names) + ".",
#               width=formatter._width,
#               initial_indent=" " * formatter._indent_increment,
#               subsequent_indent=" " * formatter._indent_increment,
#           )
#           + "\n"
#       )
# breakpoint()
# formatter = parser._get_formatter()
# formatter.start_section("See Also")
# formatter.add_text(", ".join(names) + ".")
# formatter.end_section()

# formatter._current_section.parent.start_section("See Also")
# formatter._current_section.parent.add_text(", ".join(names) + ".")
# formatter._current_section.parent.end_section()
# formatter._current_section.start_section("See Also")
# formatter._current_section.add_text(", ".join(names) + ".")
# formatter._current_section.end_section()
# formatter._root_section.parent.start_section("See Also")
# formatter._root_section.parent.add_text(", ".join(names) + ".")
# formatter._root_section.parent.end_section()


# if choice.prog == "lscolors docs":
#     breakpoint()
# if choice.description == argparse.SUPPRESS:
#     print(f"NE choice={choice} is suppressed")
# else:
# print(f"NE choice.prog={choice.prog!r} parser.prog={parser.prog!r}")
# else:
# print(f"EQ choice.prog={choice.prog!r} parser.prog={parser.prog!r}")

#       return (
#           "\n\nSee Also: \n"
#           + textwrap.fill(
#               ", ".join(names) + ".",
#               width=formatter._width,
#               initial_indent=" " * formatter._indent_increment,
#               subsequent_indent=" " * formatter._indent_increment,
#           )
#           + "\n"
#       )
