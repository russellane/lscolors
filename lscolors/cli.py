"""Command line interface."""
# /usr/lib/python3.8/argparse.py

import argparse
import sys

import argcomplete

import lscolors
import lscolors.commands
from lscolors import argformat
from lscolors.__version__ import __version__


def main():
    """Entry point."""

    parser = argparse.ArgumentParser(
        prog=__package__,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`",
        epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
    )

    argcomplete.autocomplete(parser)

    parser.add_argument(
        "-V",
        "--version",
        help="show program's version number and exit",
        action="version",
        version=__version__,
    )

    parser.set_defaults(cmd=None)
    # passing `prog` is not necessary, but speeds things up for
    # add_subparsers to not have to determine a default value for it.
    # `dest` is not necessary.
    subparsers = parser.add_subparsers(
        prog=__package__,
        metavar="COMMAND",
        title="Specify one of",
    )
    lscolors.command.Command.configure(parser, subparsers)
    for module in lscolors.commands.modules:
        module.Command()

    sub = subparsers.add_parser("help", help="same as `--help`")
    sub.set_defaults(cmd=lambda x: parser.print_help())

    argformat.argformat(parser)
    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        parser.exit(2, "error: Missing COMMAND\n")

    try:
        args.cmd(args)
    except RuntimeError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
