"""lscolors database."""

import os
import subprocess
import sys


def add_arguments(parser):
    """Add arguments to parser."""

    parser.add_argument(
        "dir_colors",
        nargs="?",
        metavar="DIR_COLORS",
        help="read file `DIR_COLORS` instead of `$LS_COLORS`",
    )


def load(args):
    """Load color database from `args.dir_colors`, if given, or `$LS_COLORS`.

    Return multiple values:
        colors: dict, colors_by_filetype, k=filetype, v=color
        meta: str, identifies database loaded and, if relevant, the `$TERM` used.
    """

    meta = f"dir_colors={args.dir_colors!r}" if args.dir_colors else "env=$LS_COLORS"
    meta_with_term = meta + "; TERM=" + os.environ.get("TERM", "")

    if args.dir_colors:
        ls_colors = _compile_dir_colors(args, meta_with_term)
    elif not (ls_colors := os.environ.get("LS_COLORS")):
        raise RuntimeError(f"missing `$LS_COLORS` environment variable; {meta}")

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


def _compile_dir_colors(args, meta):
    """Run system `dircolors` (/usr/bin/dircolors) and return value of `LS_COLORS`."""

    proc = subprocess.run(
        ["dircolors", "--bourne-shell", args.dir_colors],
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
