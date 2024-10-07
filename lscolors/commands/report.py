"""lscolors `report` command."""

from lscolors.cmd import LscolorsCmd
from lscolors.commands.utils import colors as colors_utils


class LscolorsReportCmd(LscolorsCmd):
    """lscolors `report` command."""

    def init_command(self) -> None:
        """Initialize lscolors `report` command."""

        parser = self.add_subcommand_parser(
            "report",
            help="print colorized database report",
            description="Print colorized report for database in `$LS_COLORS`.",
            epilog="A default format is produced when `--left/--right` is not given.",
        )

        grp = parser.add_mutually_exclusive_group()
        grp.add_argument(
            "--left", action="store_true", help="format report for display in left window"
        )
        grp.add_argument(
            "--right", action="store_true", help="format report for display in right window"
        )

        self.add_colors_argument(parser)

    def run(self) -> None:
        """Perform the command."""

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
            colors, meta_colors = colors_utils.load(self.options)
        except RuntimeError as err:
            raise RuntimeError(f"{self.options.prog}: failure; {err}\n") from err

        print(f"{self.options.prog} for {meta_colors}:")

        for filetype, color in colors.items():
            type_color = f"{filetype:15} {color:20}"
            _ = codes.get(filetype)
            if _:
                text = f"{_[0]} {_[1]}"
            else:
                text = filetype + " lorem ipsum dolor sit amet"

            scolor = color.ljust(10)
            if self.options.left:
                if color == "target":
                    print(f"{type_color} {scolor} {text:>44}")
                else:
                    print(f"{type_color} \x1B[{color}m{scolor} {text:>44}\x1B[0m")
            elif self.options.right:
                if color == "target":
                    print(f"{text:44} {type_color}")
                else:
                    print(f"\x1B[{color}m{text:44}\x1B[0m {type_color}")
            else:
                if color == "target":
                    print(f"{type_color} {scolor} {text:44}")
                else:
                    print(f"{type_color} \x1B[{color}m{text:44}\x1B[0m")
