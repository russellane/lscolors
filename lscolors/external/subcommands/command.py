"""Base class for all commands."""


class Command:  # noqa: SIM119 Use a dataclass
    """Base class for all commands."""

    main_parser = None
    subparsers = None
    parent = None

    def add_parser(self, name, **kwargs):
        """See /usr/lib/python3.8/argparse.py."""
        return self.subparsers.add_parser(name, **kwargs)

    @staticmethod
    def too_few_public_methods():
        """Suppress linter error in derived classes."""

    @staticmethod
    def too_few_public_methods2():
        """Suppress linter error in derived classes2."""
