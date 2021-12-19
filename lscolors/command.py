"""Base class for all commands."""


class Command:  # noqa: SIM119 Use a dataclass
    """Base class for all commands."""

    main_parser = None
    subparsers = None

    @classmethod
    def configure(cls, main_parser, subparsers):
        """Docstring."""
        cls.main_parser = main_parser
        cls.subparsers = subparsers

    @staticmethod
    def too_few_public_methods():
        """Suppress linter error in derived classes."""

    # @staticmethod
    # def horzrule(text):
    #     """Return horizontal rule with `text`."""
    #     return str(" " + text).rjust(80, "-")
