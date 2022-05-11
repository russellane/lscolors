"""Base command module."""

import argparse

from lscolors.basecli import BaseCLI


class BaseCmd:
    """Base command class."""

    def __init__(self, cli: BaseCLI) -> None:
        """Initialize base command instance."""

        self.cli = cli
        self.add_parser = self.cli.add_parser
        self.options: argparse.Namespace = None
        self.init_command()

    def init_command(self):
        """Implement in subclass to call `add_parser` and `add_argument`."""
        raise NotImplementedError

    def add_subcommand_parser(self, name, **kwargs) -> argparse._SubParsersAction:
        """Add subcommand to main parser and return subcommand's subparser.

        Wrap `ArgumentParser.add_subparsers.add_parser`.
        """

        parser = self.cli.add_parser(name, **kwargs)
        parser.set_defaults(cmd=lambda: self._promote_options(self.run), prog=name)
        return parser

    def _promote_options(self, run):
        self.options = self.cli.options
        run()

    def run(self) -> None:
        """Perform the command."""
        raise NotImplementedError
