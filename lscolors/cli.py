"""Command line interface."""
# /usr/lib/python3.8/argparse.py

import argparse
import contextlib
import importlib.metadata
import sys

import argcomplete

import lscolors.command.commands
from lscolors.external import subcommands


def main():
    """Entry point."""

    parser = argparse.ArgumentParser(
        prog=__package__,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`",
        epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
    )

    version = "0.0.0"
    with contextlib.suppress(importlib.metadata.PackageNotFoundError):
        version = importlib.metadata.version(__package__)
    parser.add_argument("-V", "--version", action="version", version=version)

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
