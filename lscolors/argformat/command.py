"""Base class for all commands."""

from lscolors import argformat


class Command:  # noqa: SIM119 Use a dataclass
    """Base class for all commands."""

    main_parser = None
    subparsers = None
    formatter_class = argformat.Argformat.FormatterClass

    @classmethod
    def add_subparsers(cls, parser, command_modules):
        """Use case 1."""

        # passing `prog` is not necessary, but speeds things up for
        # add_subparsers to not have to determine a default value for it.
        # `dest` is not necessary.
        subparsers = parser.add_subparsers(
            prog=parser.prog,
            metavar="COMMAND",
            title="Specify one of",
        )
        cls.main_parser = parser
        cls.subparsers = subparsers

        parser.set_defaults(cmd=None)
        for module in command_modules:
            module.Command()

        return subparsers

    @classmethod
    def configure(cls, main_parser=None, subparsers=None):
        """Use case 2."""
        if main_parser is not None:
            cls.main_parser = main_parser
        if subparsers is not None:
            cls.subparsers = subparsers

    # @staticmethod
    # def too_few_public_methods():
    #     """Suppress linter error in derived classes."""

    # @staticmethod
    # def horzrule(text):
    #     """Return horizontal rule with `text`."""
    #     return str(" " + text).rjust(80, "-")
