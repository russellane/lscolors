"""An `argparse` application with sub-commands."""

import lscolors.command


class Application:  # noqa: SIM119 Use a dataclass
    """An `argparse` application with sub-commands."""

    # pylint: disable=too-few-public-methods

    def __init__(self, parser, modules):
        """Initialize application.

        Args:
            parser: top-level `argparse.ArgumentParser`.
            modules: list of modules; each module must define class `Command`.
        """

        parser.set_defaults(cmd=None)
        self.subs = parser.add_subparsers(
            metavar="COMMAND", dest="command", title="Specify one of"
        )

        lscolors.command.Command.main_parser = parser
        lscolors.command.Command.subs = self.subs

        for module in modules:
            module.Command()
