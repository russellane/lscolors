"""Create documentation for Subcommands."""

import argparse
import pathlib
import textwrap

from lscolors.commands.basecmd import BaseCommand
from lscolors.commands.utils import mkdir


class Command(BaseCommand):
    """Create documentation for Subcommands."""

    def init_command(self) -> None:
        """Initialize create documentation for Subcommands."""

        parser = self.add_parser(
            "docs",
            help="create documentation",
            description="Create documentation files for this application",
            epilog="This is an internal command used during the packaging process",
        )

        parser.set_defaults(
            format="markdown",
            docs="./docs",
        )

        parser.add_argument(
            "format",
            # nargs="?",
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

    def handle(self):
        """Handle command invocation."""

        mkdir.mkdir(self.options.docs, self.options.force)
        self.print_main_page(self.cli.parser)
        self.write_command_pages(self.cli.parser, self.options.docs)

    @staticmethod
    def print_main_page(main_parser):
        """Print main help page to `stdout`."""

        print(main_parser.format_help())

    def write_command_pages(self, main_parser, directory):
        """Create separate help pages for each command in `directory`."""

        # pylint: disable=protected-access
        for action in main_parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, parser in action.choices.items():
                    helptext = parser.format_help() + self._see_also()
                    pathlib.Path(directory, name + ".txt").write_text(helptext, encoding="utf-8")

    def _see_also(self):
        """Return string with refs to other pages."""

        # pylint: disable=protected-access
        parser = self.cli.parser
        also = {}
        for action in parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name in action.choices:
                    also[name] = f"{parser.prog}-{name}"
        if not also:
            return ""

        formatter = parser._get_formatter()
        return "\n\nSee Also: \n" + textwrap.fill(
            ", ".join(also.values()) + ".",
            width=formatter._width,
            initial_indent=" " * formatter._indent_increment,
            subsequent_indent=" " * formatter._indent_increment,
        )
