"""Commands."""

from lscolors.commands.chart import ChartCmd
from lscolors.commands.check import CheckCmd
from lscolors.commands.configs import ConfigsCmd
from lscolors.commands.docs import DocsCmd
from lscolors.commands.paint import PaintCmd
from lscolors.commands.report import ReportCmd
from lscolors.commands.samples import SamplesCmd
from lscolors.commands.sort import SortCmd

CLASSES = [
    ChartCmd,
    CheckCmd,
    ConfigsCmd,
    DocsCmd,
    PaintCmd,
    ReportCmd,
    SamplesCmd,
    SortCmd,
]
