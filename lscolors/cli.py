"""Command line interface."""

import argparse
import sys

import argcomplete

import lscolors
import lscolors.commands
from lscolors.__version__ import __version__


def main():
    """Entry point."""

    parser = argparse.ArgumentParser(
        prog=__package__,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`",
        epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
    )

    parser.add_argument(
        "-V",
        "--version",
        help="show program's version number and exit",
        action="version",
        version=__version__,
    )

    app = lscolors.command.CommandApp(parser, lscolors.commands.modules)

    sub = app.subs.add_parser("help", help="same as `--help`")
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
