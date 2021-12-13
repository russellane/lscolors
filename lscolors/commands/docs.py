"""lscolors `docs` command."""

import argparse
import pathlib

import lscolors.mkdir


def add_parser(subs, main_parser):
    """Add command parser."""

    parser = subs.add_parser(
        "docs",
        help="Create documentation for this application" "",
        description="""\
This application's packaging process uses this internal
command to create this application's documentation.""",
    )

    parser.set_defaults(
        cmd=_handle,
        prog="lscolors docs",
        docs="./docs",
        main_parser=main_parser,
    )

    parser.add_argument(
        "docs",
        nargs="?",
        metavar="DIR",
        help="create directory `DIR`. " f"(default: {parser.get_default('docs')!r})",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Ok to clobber `DIR` if it exists"
    )


def _handle(args):

    lscolors.mkdir.mkdir(args.docs, args.force)

    # pylint: disable=protected-access
    for action in args.main_parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, parser in action.choices.items():
                path = pathlib.Path(args.docs, name)
                with open(path, "w", encoding="utf-8") as file:
                    parser.print_help(file=file)
