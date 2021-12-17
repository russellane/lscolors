"""Base class for all commands."""


class Command:
    """Base class for all lscolors commands."""

    # pylint: disable=too-few-public-methods

    main_parser = None
    subs = None

    def __init__(self):
        """Initialize base of all commands."""

    @staticmethod
    def horzrule(text):
        """Return horizontal rule with `text`."""

        return str(" " + text).rjust(80, "-")


# -------------------------------------------------------------------------------


class CommandApp:  # noqa: SIM119 Use a dataclass
    """Application whose functionality is split into a number of sub-commands."""

    # pylint: disable=too-few-public-methods

    def __init__(self, parser, modules):
        """Initialize application.

        Args:
            parser: top-level `argparse.ArgumentParser`.
            modules: list of modules; each defines a Command class.
        """

        parser.set_defaults(cmd=None)
        self.subs = parser.add_subparsers(
            metavar="COMMAND", dest="command", title="Specify one of"
        )

        Command.main_parser = parser
        Command.subs = self.subs

        for module in modules:
            module.Command()
