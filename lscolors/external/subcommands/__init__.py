"""Docstring."""

from . import command


class Subcommands:  # noqa: SIM119 Use a dataclass
    """Docstring."""

    # pylint: disable=too-few-public-methods

    def __init__(self, parser, command_modules):
        """Docstring."""

        # passing `prog` is not necessary, but speeds things up for
        # add_subparsers to not have to determine a default value for it.
        # `dest` is not necessary.

        self.subparsers = parser.add_subparsers(
            prog=parser.prog,
            metavar="COMMAND",
            title="Specify one of",
        )

        # configure Command class
        command.Command.main_parser = parser
        command.Command.formatter_class = parser.formatter_class
        command.Command.subparsers = self.subparsers

        parser.set_defaults(cmd=None)
        for module in command_modules:
            module.Command()


# -------------------------------------------------------------------------------


def add_subcommands(parser, command_modules):
    """Wrapper similar to `argparse.ArgumentParser.add_subparsers`."""

    subcommands = Subcommands(parser, command_modules)
    return subcommands.subparsers
