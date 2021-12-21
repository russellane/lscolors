"""lscolors `docs` command."""

# move this into argformat

import lscolors
import lscolors.argformat


class Command(lscolors.command.Command):
    """lscolors `docs` command."""

    def __init__(self):
        """Initialize lscolors `docs` command."""

        parser = self.subparsers.add_parser(
            "docs",
            formatter_class=self.formatter_class,
            help="Create documentation.",
            description="Create documentation files for this application.",
            epilog="This is an internal command used during the packaging process.",
        )

        parser.set_defaults(
            cmd=self.handle,
            prog="lscolors docs",
            format="markdown",
            docs="./docs",
        )

        parser.add_argument(
            "format",
            choices=["ansi", "md", "txt"],
            help="Output format",
        )

        parser.add_argument(
            "docs",
            metavar="DIR",
            help="create directory `DIR`. " f"(default: {parser.get_default('docs')!r})",
        )

        parser.add_argument(
            "-f",
            "--force",
            action="store_true",
            help="Ok to clobber `DIR` if it exists",
        )

    def handle(self, args):
        """Handle command invocation."""

        lscolors.mkdir.mkdir(args.docs, args.force)
        lscolors.argformat.configure(format=args.format)
        lscolors.argformat.print_main_page(self.main_parser)
        lscolors.argformat.write_command_pages(self.main_parser, args.docs)
