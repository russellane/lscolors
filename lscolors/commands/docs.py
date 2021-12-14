"""lscolors `docs` command."""

import argparse
import pathlib

import mandown.mandown

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
    also = _see_also(args)

    # pylint: disable=protected-access
    for action in args.main_parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name, parser in action.choices.items():
                lines = parser.format_help().splitlines()
                see_also = ", ".join([v for k, v in also.items() if k != name]) + "."
                mdoc = mandown.mandown.Mandown(lines, name=f"lscolors-{name}", see_also=see_also)
                text = mdoc.render_markdown()
                pathlib.Path(args.docs, name + ".md").write_text(text, encoding="utf-8")


def _see_also(args):
    """Docstring."""

    also = {}

    # pylint: disable=protected-access
    for action in args.main_parser._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            for name in action.choices:
                also[name] = f"[lscolors-{name}]({name}.md)"

    return also
