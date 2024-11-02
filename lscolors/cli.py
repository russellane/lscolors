"""Command line interface."""

import sys

from libcli import BaseCLI

__all__ = ["LscolorsCLI"]


class LscolorsCLI(BaseCLI):
    """Command line interface."""

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.ArgumentParser(
            prog=__package__,
            description="Utilities for `dircolors(1)` and `dir_colors(5)`.",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.add_subcommand_modules("lscolors.commands", prefix="Lscolors", suffix="Cmd")

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        try:
            self.options.cmd()
        except RuntimeError as err:
            print(err, file=sys.stderr)
            sys.exit(1)


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    LscolorsCLI(args).main()
