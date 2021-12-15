"""lscolors `report` command."""

import lscolors.colors


def add_parser(subs):
    """Add command parser."""

    parser = subs.add_parser(
        "report",
        help="print colorized database report",
        description="Print colorized report for database in `$LS_COLORS`.",
        epilog="A default format is produced when `--left/--right` is not given.",
    )

    parser.set_defaults(cmd=_handle, prog="lscolors report")

    grp = parser.add_mutually_exclusive_group()
    grp.add_argument(
        "--left", action="store_true", help="format report for display in left window"
    )
    grp.add_argument(
        "--right", action="store_true", help="format report for display in right window"
    )

    lscolors.colors.add_arguments(parser)


def _handle(args):

    codes = {
        "no": ("NORMAL", "- Normal (nonfilename) text"),
        "fi": ("FILE", "- Regular File"),
        "di": ("DIR", "- Directory"),
        "ln": ("LINK", "- Symbolic Link"),
        "pi": ("FIFO", "- Named Pipe"),
        "so": ("SOCK", "- Unix Domain Socket"),
        "do": ("DOOR", "- Door"),
        "bd": ("BLK", "- Block Device"),
        "cd": ("CHR", "- Character Device"),
        "or": ("ORPHAN", "- Orphaned Symbolic Link"),
        "mi": ("MISSING", "- Missing File"),
        "su": ("SETUID", "- Set User ID"),
        "sg": ("SETGID", "- Set Group ID"),
        "tw": ("STICKY_OTHER_WRITABLE", ""),
        "ow": ("OTHER_WRITABLE", "- Other Writable"),
        "st": ("STICKY", "- Sticky"),
        "ex": ("EXEC", "- Executable"),
        "rs": ("RESET", "- Reset to NORMAL"),
        "mh": ("MULTIHARDLINK", "- Multiple Hard Links"),
        "ca": ("CAPABILITY", ""),
    }

    try:
        colors, meta_colors = lscolors.colors.load(args)
    except RuntimeError as err:
        raise RuntimeError(f"{args.prog}: failure; {err}\n") from err

    print(f"{args.prog} for {meta_colors}:")

    for filetype, color in colors.items():
        type_color = f"Type: {filetype:15} Colour: {color:20}"
        _ = codes.get(filetype)
        if _:
            text = f"{_[0]} {_[1]}"
        else:
            text = filetype + " (TODO: get description)"

        if args.left:
            if color == "target":
                print(f"{type_color} {text:>40}")
            else:
                print(f"{type_color} [{color}m{color} {text:>40}[0m")
        elif args.right:
            if color == "target":
                print(f"{text:40} {type_color}")
            else:
                print(f"[{color}m{text:40}[0m {type_color}")
        else:
            if color == "target":
                print(f"{type_color} {text:40}")
            else:
                print(f"{type_color} [{color}m{text:40}[0m")
