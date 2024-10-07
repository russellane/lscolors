"""lscolors database."""

import os
import subprocess
import sys
from argparse import ArgumentParser, Namespace

from libcli import BaseCLI


def add_colors_argument(cli: BaseCLI, parser: ArgumentParser) -> None:
    """Add arguments to parser."""

    _ = cli  # unused

    parser.add_argument(
        "dir_colors",
        nargs="?",
        metavar="DIR_COLORS",
        help="read file `DIR_COLORS` instead of `$LS_COLORS`",
    )


def load(options: Namespace) -> tuple[dict[str, str], str]:
    """Load color database from `options.dir_colors`, if given, or `$LS_COLORS`.

    Return multiple values:
        colors: dict, colors_by_filetype, k=filetype, v=color
        meta: str, identifies database loaded and, if relevant, the `$TERM` used.
    """

    meta = f"dir_colors={options.dir_colors!r}" if options.dir_colors else "env=$LS_COLORS"
    meta_with_term = meta + "; TERM=" + os.environ.get("TERM", "")

    if options.dir_colors:
        ls_colors = _compile_dir_colors(options, meta_with_term)
    elif not (_ls_colors := os.environ.get("LS_COLORS")):
        raise RuntimeError(f"missing `$LS_COLORS` environment variable; {meta}")
    else:
        ls_colors = _ls_colors

    if ls_colors:
        ls_colors = ls_colors.strip(":")
    if not ls_colors:
        raise RuntimeError(f"empty database; {meta_with_term}")

    #
    colors = {}
    for item in ls_colors.split(":"):
        filetype, color = item.split("=")
        if filetype.startswith("*."):
            filetype = filetype[1:]
        colors[filetype] = color

    return colors, meta


def _compile_dir_colors(options: Namespace, meta: str) -> str:
    """Run system `dircolors` (/usr/bin/dircolors) and return value of `LS_COLORS`."""

    proc = subprocess.run(
        ["dircolors", "--bourne-shell", options.dir_colors],
        capture_output=True,
        check=False,
        shell=False,
        text=True,
    )

    if proc.returncode:
        print(proc.stderr.strip(), file=sys.stderr)
        raise RuntimeError(f"system dircolors; {meta}")

    ls_colors = proc.stdout.strip()
    len1 = len("LS_COLORS='")
    len2 = len("';\nexport LS_COLORS")
    if len(ls_colors) >= len1 + len2:
        ls_colors = ls_colors[len1:-len2]

    return ls_colors
