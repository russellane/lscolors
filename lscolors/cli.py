"""Command line interface."""

import sys
from typing import List, Optional

import lscolors.commands
from lscolors.basecli import BaseCLI


class CLI(BaseCLI):
    """Command line interface."""

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.parser = self.ArgumentParser(
            prog=__package__,
            description="Utilities for `dircolors(1)` and `dir_colors(5)`.",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.add_subcommand_classes(lscolors.commands.CLASSES)

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        try:
            self.options.cmd()
        except RuntimeError as err:
            print(err, file=sys.stderr)
            sys.exit(1)


def main(args: Optional[List[str]] = None) -> None:
    """Command line interface entry point (function)."""
    return CLI(args).main()
