"""Base class for all commands."""

import argparse

from lscolors.basecli import BaseCLI


class BaseCommand:  # noqa: SIM119 Use a dataclass
    """Base class for all commands."""

    add_period_to_help = True

    def __init__(self, cli: BaseCLI) -> None:
        """Initialize command."""
        self.cli = cli
        self.init_command()

    def init_command(self) -> None:
        """Implement in subclass, if desired."""

    def add_parser(self, name, **kwargs) -> argparse.ArgumentParser:
        """See /usr/lib/python3.8/argparse.py."""
        kwargs["formatter_class"] = self.cli.parser.formatter_class
        if self.add_period_to_help and (text := kwargs.get("help")) and not text.endswith("."):
            kwargs["help"] += "."
        parser = self.cli.subparsers.add_parser(name, **kwargs)
        self.cli.add_verbose_option(parser)
        self.cli.add_version_option(parser)
        parser.set_defaults(cmd=self.handle, prog=name)
        return parser

    def handle(self, args):  # RENAME args to options
        """Handle command invocation."""
        raise NotImplementedError

    @staticmethod
    def too_few_public_methods():
        """Suppress linter error in derived classes."""

    @staticmethod
    def too_few_public_methods2():
        """Suppress linter error in derived classes2."""
