"""lscolors `configs` command."""

import os.path

import lscolors


class Command(lscolors.Command):
    """lscolors `configs` command."""

    def __init__(self):
        """Initialize lscolors `configs` command."""

        parser = self.add_parser(
            "configs",
            help="print path to sample configuration files",
            formatter_class=self.formatter_class,
            description="""Print path to sample `.lscolors.yml`
                            and `.dircolors` configuration files.""",
        )

        parser.set_defaults(cmd=self.handle, prog="lscolors configs")

    @staticmethod
    def handle(args):
        """Handle command invocation."""

        _ = args  # unused
        print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample-configs"))
