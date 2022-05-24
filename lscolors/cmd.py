"""Lscolors base command."""

import argparse

from libcli import BaseCmd

import lscolors.commands.utils.colors
import lscolors.commands.utils.config


class LscolorsCmd(BaseCmd):
    """Lscolors base command class."""

    def init_command(self) -> None:
        """Initialize."""

    def run(self) -> None:
        """Perform."""

    def add_config_option(self, parser: argparse.ArgumentParser) -> None:
        """Add `--config` option."""
        lscolors.commands.utils.config.add_config_option(self.cli, parser)

    def add_colors_argument(self, parser: argparse.ArgumentParser) -> None:
        """Add `DIR_COLORS` argument."""
        lscolors.commands.utils.colors.add_colors_argument(self.cli, parser)
