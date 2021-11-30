"""Command line interface."""

import argparse
import sys

import argcomplete

import lscolors.chart
import lscolors.check
import lscolors.configs
import lscolors.report
import lscolors.samples
import lscolors.sort
from lscolors.__version__ import __version__


def main():
    """Entry point."""

    prog = "lscolors"

    parser = argparse.ArgumentParser(
        prog=prog,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`.",
        epilog=f"See `{prog} COMMAND --help` for help on a specific command.",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)

    subs = parser.add_subparsers(metavar="COMMAND", dest="command", title="Specify one of")
    parser.set_defaults(cmd=None, prog=prog)

    lscolors.chart.add_parser(subs)
    lscolors.check.add_parser(subs)
    lscolors.configs.add_parser(subs)
    lscolors.report.add_parser(subs)
    lscolors.samples.add_parser(subs)
    lscolors.sort.add_parser(subs)

    sub = subs.add_parser("help", help="same as `--help`")
    sub.set_defaults(cmd=lambda x: parser.print_help())

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        parser.exit(2, "error: Missing COMMAND\n")

    try:
        args.cmd(args)
    except SyntaxError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
