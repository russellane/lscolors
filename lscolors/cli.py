"""Command line interface."""

import argparse
import sys

import argcomplete

import lscolors.commands.chart
import lscolors.commands.check
import lscolors.commands.configs
import lscolors.commands.docs
import lscolors.commands.report
import lscolors.commands.samples
import lscolors.commands.sort
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

    parser.add_argument(
        "--test-one",
        nargs="?",
        metavar="FILE",
        help="test option for testing",
    )

    parser.add_argument(
        "--test-two",
        nargs="?",
        metavar="FILE",
        help="another test option for testing",
    )

    parser.set_defaults(cmd=None)
    subs = parser.add_subparsers(metavar="COMMAND", dest="command", title="Specify one of")

    lscolors.commands.chart.add_parser(subs)
    lscolors.commands.check.add_parser(subs)
    lscolors.commands.configs.add_parser(subs)
    lscolors.commands.docs.add_parser(subs, parser)
    lscolors.commands.report.add_parser(subs)
    lscolors.commands.samples.add_parser(subs)
    lscolors.commands.sort.add_parser(subs)

    sub = subs.add_parser("help", help="same as `--help`")
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
