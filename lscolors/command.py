"""Base class for all commands."""


class Command:  # noqa: SIM119 Use a dataclass
    """Base class for all commands."""

    # pylint: disable=too-few-public-methods

    main_parser = None
    subs = None

    def __init__(self):
        """Initialize base of all commands."""

    @staticmethod
    def too_few_public_methods():
        """Suppress linter error in derived classes."""

    # @staticmethod
    # def horzrule(text):
    #     """Return horizontal rule with `text`."""
    #     return str(" " + text).rjust(80, "-")
