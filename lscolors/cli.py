"""lscolors command line interface."""
# -------------------------------------------------------------------------------

import argparse
import os.path
import sys

import argcomplete

import lscolors.chart
import lscolors.check
import lscolors.report
import lscolors.samples
import lscolors.sort

# -------------------------------------------------------------------------------


def main():
    """Command line interface entry point.

    See setuptools.setup(entry_points={'console_scripts': ['lscolors=lscolors.cli:main']})
    """

    prog = "lscolors"

    parser = argparse.ArgumentParser(
        prog=prog,
        description="Utilities for `dircolors(1)` and `dir_colors(5)`.",
        epilog=f"See `{prog} COMMAND --help` for help on a specific command.",
    )

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
    if not args.cmd:
        parser.print_help()
        parser.exit(2, "error: Missing COMMAND\n")

    try:
        args.cmd(args)
    except SyntaxError as err:
        print(err, file=sys.stderr)
        sys.exit(1)


# -------------------------------------------------------------------------------
