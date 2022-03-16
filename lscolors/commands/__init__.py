"""lscolors commands."""

# from lscolors.external.subcommands import docs

from lscolors.commands.chart import ChartCommand
from lscolors.commands.check import CheckCommand
from lscolors.commands.configs import ConfigsCommand
from lscolors.commands.paint import PaintCommand
from lscolors.commands.report import ReportCommand
from lscolors.commands.samples import SamplesCommand
from lscolors.commands.sort import SortCommand

modules = (
    ChartCommand,
    CheckCommand,
    ConfigsCommand,
    PaintCommand,
    ReportCommand,
    SamplesCommand,
    SortCommand,
)
