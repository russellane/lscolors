"""lscolors `configs` command."""

import os.path

from lscolors.basecmd import BaseCmd


class ConfigsCmd(BaseCmd):
    """lscolors `configs` command."""

    def init_command(self) -> None:
        """Initialize lscolors `configs` command."""

        self.add_subcommand_parser(
            "configs",
            help="print path to sample configuration files",
            description="""Print path to sample `.lscolors.yml`
                            and `.dircolors` configuration files.""",
        )

    def run(self):
        """Perform the command."""

        _ = self  # unused

        print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample-configs"))
