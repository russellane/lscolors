"""Command line interface."""

import sys
from typing import List, Optional

from lscolors.basecli import BaseCLI
from lscolors.commands.basecmd import BaseCommand
from lscolors.commands.chart import Command as ChartCommand
from lscolors.commands.check import Command as CheckCommand
from lscolors.commands.configs import Command as ConfigsCommand
from lscolors.commands.docs import Command as DocsCommand
from lscolors.commands.paint import Command as PaintCommand
from lscolors.commands.report import Command as ReportCommand
from lscolors.commands.samples import Command as SamplesCommand
from lscolors.commands.sort import Command as SortCommand

# from lscolors.commands.doc?


class CLI(BaseCLI):
    """Command line interface."""

    def init_parser(self) -> None:
        """Initialize main argument parser."""

        self.parser = self.ArgumentParser(
            prog=__package__,
            description="Utilities for `dircolors(1)` and `dir_colors(5)`",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add command arguments (subparsers) to main parser."""

        # passing `prog` is not necessary, but speeds things up for
        # add_subparsers to not have to determine a default value for it.
        # `dest` is not necessary.

        # alternate design: self.parser.init_subparsers(...)
        self.subparsers = self.parser.add_subparsers(
            prog=self.parser.prog,
            metavar="COMMAND",
            title="Specify one of",
        )

        # configure BaseCommand class
        BaseCommand.cli = self

        self.parser.set_defaults(cmd=None)

        for command_class in (
            ChartCommand,
            CheckCommand,
            ConfigsCommand,
            DocsCommand,
            PaintCommand,
            ReportCommand,
            SamplesCommand,
            SortCommand,
        ):
            command_class()
            # parser = cli.init_subparser(self)
            # self.add_parser(parser)
            # self.subparsers.add_parser(parser)

        # equiv to module: lscolors.commands.help import Command as HelpCommand
        sub = self.subparsers.add_parser("help", help="same as `--help`")
        sub.set_defaults(cmd=lambda x: self.parser.print_help())

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        try:
            self.options.cmd(self.options)
        except RuntimeError as err:
            print(err, file=sys.stderr)
            sys.exit(1)


def main(args: Optional[List[str]] = None) -> None:
    """Command line interface entry point (function)."""
    return CLI(args).main()
