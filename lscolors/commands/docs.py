"""lscolors `docs` command."""

import lscolors.mandown_  # developing here for now; to be moved to mandown.mandown
import lscolors.mkdir

# -------------------------------------------------------------------------------


def add_parser(subs, main_parser):
    """Add command parser."""

    parser = subs.add_parser(
        "docs",
        help="Create documentation for this application" "",
        description="Woohoo.",
        epilog="""\
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
        "-f",
        "--force",
        action="store_true",
        help="Ok to clobber `DIR` if it exists",
    )

    parser.add_argument(
        "--top-level",
        action="store_true",
        help="Create top level page only",
    )


# -------------------------------------------------------------------------------


def _handle(args):

    if args.top_level:
        lscolors.mandown_.print_main_page(args.main_parser)
    else:
        lscolors.mkdir.mkdir(args.docs, args.force)
        lscolors.mandown_.write_command_pages(args.main_parser, args.docs)
