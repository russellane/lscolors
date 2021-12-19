"""lscolors `docs` command."""

import lscolors
import lscolors.mandown_  # developing here for now; to be moved to mandown.mandown


class Command(lscolors.command.Command):
    """lscolors `docs` command."""

    def __init__(self):
        """Initialize lscolors `docs` command."""

        parser = self.subparsers.add_parser(
            "docs",
            help="Create documentation.",
            description="Create documentation files for this application.",
            epilog="This is an internal command used during the packaging process.",
        )

        parser.set_defaults(
            cmd=self.handle,
            prog="lscolors docs",
            docs="./docs",
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

    def handle(self, args):
        """Handle command invocation."""

        if args.top_level:
            lscolors.mandown_.print_main_page(self.main_parser)
        else:
            lscolors.mkdir.mkdir(args.docs, args.force)
            lscolors.mandown_.write_command_pages(self.main_parser, args.docs)
