"""lscolors `configs` command."""

import os.path

from lscolors.basecli import BaseCommand


class Command(BaseCommand):
    """lscolors `configs` command."""

    def init_command(self) -> None:
        """Initialize lscolors `configs` command."""

        self.add_parser(
            "configs",
            help="print path to sample configuration files",
            description="""Print path to sample `.lscolors.yml`
                            and `.dircolors` configuration files.""",
        )

    @staticmethod
    def handle():
        """Handle command invocation."""

        print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample-configs"))
