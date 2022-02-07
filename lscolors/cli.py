"""Command line interface."""

import sys

import argcomplete
import argparse_color as argparse

import lscolors.command.commands
from lscolors.__version__ import __version__
from lscolors.external import subcommands


def main():
    """Entry point."""

    parser = argparse.ArgumentParser(
        prog=__package__,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`",
        epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
    )

    subcommands.add_subcommands(parser, lscolors.command.commands.modules, version=__version__)
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
