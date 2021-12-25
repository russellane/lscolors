"""lscolors commands."""

from lscolors.external.subcommands import docs

# from . import docs
from . import chart
from . import check
from . import configs
from . import report
from . import samples
from . import sort

modules = [
    chart,
    check,
    configs,
    docs,
    report,
    samples,
    sort,
]
