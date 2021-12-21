"""Base class for all commands."""

from lscolors import argformat


class Command:  # noqa: SIM119 Use a dataclass
    """Base class for all commands."""

    main_parser = None
    subparsers = None
    formatter_class = argformat.ansi.AnsiHelpFormatter

    # pylint: disable=redefined-builtin
    @classmethod
    def configure(cls, main_parser=None, subparsers=None, format=None):
        """Docstring."""
        if main_parser is not None:
            cls.main_parser = main_parser
        if subparsers is not None:
            cls.subparsers = subparsers
        if format is not None:
            argformat.configure(format=format)
            cls.formatter_class = argformat.Argformat.FormatterClass

    @staticmethod
    def too_few_public_methods():
        """Suppress linter error in derived classes."""

    # @staticmethod
    # def horzrule(text):
    #     """Return horizontal rule with `text`."""
    #     return str(" " + text).rjust(80, "-")
