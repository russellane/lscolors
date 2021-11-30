"""lscolors `configs` command."""

import os.path


def add_parser(subs):
    """Add command parser."""

    parser = subs.add_parser(
        "configs",
        help="print path to sample configuration files",
        description="""Print path to sample `.lscolors.yml`
                          and `.dircolors` configuration files.""",
    )

    parser.set_defaults(cmd=_handle, prog="lscolors configs")


def _handle(args):

    _ = args  # unused
    print(os.path.join(os.path.dirname(__file__), "sample-configs"))
