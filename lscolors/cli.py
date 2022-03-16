"""Command line interface."""

import argparse
import contextlib
import importlib.metadata
import sys
from typing import List, Optional

import argcomplete

from lscolors import Lscolors

modules = [
    chart,
    check,
    configs,
    # docs,
    paint,
    report,
    samples,
    sort,
]


class CLI(CLIBase):
    """Command line interface."""

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.parser = self.ArgumentParser(
            prog=__package__,
            description="Utilities for `dircolors(1)` and `dir_colors(5)`",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        # passing `prog` is not necessary, but speeds things up for
        # add_subparsers to not have to determine a default value for it.
        # `dest` is not necessary.

        self.subparsers = self.parser.add_subparsers(
            prog=self.parser.prog,
            metavar="COMMAND",
            title="Specify one of",
        )

        print("type(self.parser.prog)", repr(type(self.parser.prog)))

        self.parser.set_defaults(cmd=None)
        for module in command_modules:
            module.Command()

    subparsers = subcommands.add_subcommands(parser, lscolors.command.commands.modules)

    sub = subparsers.add_parser("help", help="same as `--help`")
    sub.set_defaults(cmd=lambda x: parser.print_help())

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        parser.exit(2, "error: Missing COMMAND\n")

    try:
        args.cmd(args)
    except RuntimeError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

    # -------------------------------------------------------------------------------

    def main(self) -> None:
        """Command line interface entry point (method)."""

        Lscolors(options)


# -------------------------------------------------------------------------------


def main(args: Optional[List[str]] = None) -> None:
    """Command line interface entry point (function)."""
    return CLI(args).main()
