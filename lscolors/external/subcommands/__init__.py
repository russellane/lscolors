"""Docstring."""

import argparse_color as argparse
import icecream
from icecream import ic

from . import command
from . import docs as _docs

icecream.install()
ic.configureOutput(prefix="\nic ===> ", includeContext=True)


class Subcommands:  # noqa: SIM119 Use a dataclass
    """Docstring."""

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        parser,
        command_modules,
        /,
        version=None,
        add_help=True,
        show_help=False,
        add_docs=True,
        show_docs=False,
    ):
        """Docstring."""

        self.subparsers = parser.add_subparsers(
            # passing `prog` is not necessary, but speeds things up for
            # add_subparsers to not have to determine a default value for it.
            # `dest` is not necessary.
            prog=parser.prog,
            metavar="COMMAND",
            title="Specify one of",
        )

        # configure Command class
        command.Command.main_parser = parser
        command.Command.subparsers = self.subparsers
        command.Command.parent = self
        ic(self.__dict__)

        parser.set_defaults(cmd=None)
        for module in command_modules:
            module.Command()

        if version:
            parser.add_argument(
                "-V",
                "--version",
                help="show program's version number and exit",
                action="version",
                version=version,
            )

        if add_help:
            sub = self.subparsers.add_parser(
                "help",
                help="same as `--help`" if show_help else argparse.SUPPRESS,
            )
            sub.set_defaults(cmd=lambda x: parser.print_help())

        self.show_docs = add_docs and show_docs
        if add_docs:
            _docs.Command()


# -------------------------------------------------------------------------------


def add_subcommands(
    parser,
    command_modules,
    /,
    version=None,
    add_help=True,
    show_help=False,
    add_docs=True,
    show_docs=False,
):
    """Similar to calling `argparse.ArgumentParser.add_subparsers` and returning its result."""

    subcommands = Subcommands(
        parser,
        command_modules,
        version,
        add_help,
        show_help,
        add_docs,
        show_docs,
    )
    return subcommands.subparsers
