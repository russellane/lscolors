"""lscolors commands."""

import lscolors.argformat.command
import lscolors.commands.chart
import lscolors.commands.check
import lscolors.commands.configs
import lscolors.commands.docs
import lscolors.commands.report
import lscolors.commands.samples
import lscolors.commands.sort


def configure(parser, subparsers):
    """Load all command modules."""

    lscolors.argformat.command.Command.configure(parser, subparsers)

    for module in [
        lscolors.commands.chart,
        lscolors.commands.check,
        lscolors.commands.configs,
        lscolors.commands.docs,
        lscolors.commands.report,
        lscolors.commands.samples,
        lscolors.commands.sort,
    ]:
        module.Command()
