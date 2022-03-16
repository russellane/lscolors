"""lscolors `docs` command."""

# move this into argformat

from lscolors.commands.base import BaseCommand

# from lscolors.external import argformat


class Command(BaseCommand):
    """lscolors `docs` command."""

    def __init__(self):
        """Initialize lscolors `docs` command."""

        parser = self.add_parser(
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

        lscolors.mkdir(args.docs, args.force)
        _ = self
        # argformat.configure(format=args.format)
        # argformat.print_main_page(self.main_parser)
        # argformat.write_command_pages(self.main_parser, args.docs)
