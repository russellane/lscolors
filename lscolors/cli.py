"""Command line interface."""

import argparse
import importlib.metadata
import os.path
import sys

import argcomplete

import lscolors.chart
import lscolors.check
import lscolors.report
import lscolors.samples
import lscolors.sort

try:
    __version__ = importlib.metadata.version("rlane-lscolors")
except importlib.metadata.PackageNotFoundError:
    __version__ = "not installed"


def main():
    """Entry point."""

    prog = "lscolors"

    parser = argparse.ArgumentParser(
        prog=prog,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`.",
        epilog=f"See `{prog} COMMAND --help` for help on a specific command.",
    )
    parser.add_argument("-V", "--version", action="store_true", help="print version and exit")

    subs = parser.add_subparsers(metavar="COMMAND", dest="command", title="Specify one of")
    parser.set_defaults(cmd=None, prog=prog)

    lscolors.chart.add_parser(subs)
    lscolors.check.add_parser(subs)

    sub = subs.add_parser(
        "configs",
        help="print path to sample configuration files.",
        description="""Print path to sample `.lscolors.yml`
                          and `.dircolors` configuration files.""",
    )
    sub.set_defaults(
        cmd=lambda x: print(os.path.join(os.path.dirname(__file__), "sample-configs"))
    )

    lscolors.report.add_parser(subs)
    lscolors.samples.add_parser(subs)
    lscolors.sort.add_parser(subs)

    sub = subs.add_parser("help", help="same as `--help`.")
    sub.set_defaults(cmd=lambda x: parser.print_help())

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if not args.cmd:
        parser.print_help()
        parser.exit(2, "error: Missing COMMAND\n")

    try:
        args.cmd(args)
    except SyntaxError as err:
        print(err, file=sys.stderr)
        sys.exit(1)
