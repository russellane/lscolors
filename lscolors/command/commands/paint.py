"""lscolors `paint` command."""

import re
import sys
from pathlib import Path

from colors.colors import parse_rgb

import lscolors


class ColorGroup:
    """Color for collection of files."""

    _group_by_name = {}
    _group_by_comment = {}

    @classmethod
    def get_by_name(cls, name, default=None):
        """Return ColorGroup with matching `name`."""
        return cls._group_by_name.get(name, default)

    @classmethod
    def get_by_comment(cls, comment, default=None):
        """Return ColorGroup with matching `comment`."""
        return cls._group_by_comment.get(comment, default)

    @classmethod
    def items(cls):
        """Return list of ColorGroup's in insertion order."""
        yield from cls._group_by_name.values()

    # https://stackoverflow.com/questions/11765623/convert-hex-to-closest-x11-color-number
    _closest_colors = []
    for i, num in enumerate([47, 68, 40, 40, 40, 21]):
        _closest_colors.extend([i] * num)
    _re_rgb = re.compile(r"[0-9A-Fa-f]{6}")

    @classmethod
    def rgb_to_xterm(cls, rgb):
        """Return xterm color index from rgb tuple."""

        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        max_ = max(red, green, blue)
        min_ = min(red, green, blue)

        if (max_ - min_) * (max_ + min_) <= 6250:
            color = 24 - (252 - ((red + green + blue) // 3)) // 10
            if 0 <= color <= 23:
                return 232 + color

        return (
            16
            + 36 * cls._closest_colors[red]
            + 6 * cls._closest_colors[green]
            + cls._closest_colors[blue]
        )

    def __init__(self, name, comment=None):
        """Add new ColorGroup to pool.

        Args:
            name: name of ColorGroup.
            comment: line to match in `dir_colors(5)` file.
        """

        self.group_name = name
        self.comment = comment
        self.color_name = None
        self.ansi = None
        self.rgb = None

        self.__class__._group_by_name[self.group_name] = self
        if self.comment:
            self.__class__._group_by_comment[self.comment] = self

    def set_color(self, color):
        """Assign `color` to this ColorGroup."""

        try:
            self.rgb = color
            rgb = parse_rgb(self.rgb)
            self.ansi = "38;5;" + str(ColorGroup.rgb_to_xterm(rgb))
        except ValueError:
            self.ansi = color


class Command(lscolors.Command):
    """lscolors `paint` command."""

    # default groups
    ColorGroup("archive", " # archives or compressed (bright red)")
    ColorGroup("image", "# image formats")
    ColorGroup("audio", "# audio formats")

    # our additions
    ColorGroup("data", "# data")
    ColorGroup("source", "# source")
    ColorGroup("config", "# config")
    ColorGroup("history", "# history")
    ColorGroup("doc", "# doc")

    for filetype in [
        "NORMAL",
        "FILE",
        "RESET",
        "DIR",
        "LINK",
        "MULTIHARDLINK",
        "FIFO",
        "SOCK",
        "DOOR",
        "BLK",
        "CHR",
        "ORPHAN",
        "MISSING",
        "SETUID",
        "SETGID",
        "CAPABILITY",
        "STICKY_OTHER_WRITABLE",
        "OTHER_WRITABLE",
        "STICKY",
        "EXEC",
    ]:
        ColorGroup(filetype)

    def __init__(self):
        """Initialize lscolors `paint` command."""

        parser = self.add_parser(
            "paint",
            formatter_class=self.formatter_class,
            help="paint dircolors",
            description="Apply palette to dircolors.",
        )

        parser.set_defaults(cmd=self.handle, prog="lscolors paint")

        default_config_path = Path.home() / ".dircolors"
        parser.add_argument(
            "dir_colors",
            nargs="?",
            metavar="DIR_COLORS",
            type=Path,
            default=default_config_path,
            help=f"read `DIR_COLORS` file (default: `{default_config_path}`)",
        )

        default_encoding = "utf-8"
        parser.add_argument(
            "--encoding",
            metavar="NAME",
            default=default_encoding,
            help=f"file encoding (default: `{default_encoding}`)",
        )

        default_palettes_dir = Path.home() / ".palettes"
        parser.add_argument(
            "--palettes-dir",
            metavar="DIR",
            type=Path,
            default=default_palettes_dir,
            help=f"directory of `coloors.co` palettes (default: `{default_palettes_dir}`)",
        )

        parser.add_argument(
            "--palette-num",
            metavar="NUMBER",
            type=int,
            help="id of `coloors.co` palette file to apply",
        )

        parser.add_argument(
            "--palette-file",
            metavar="FILE",
            type=Path,
            help="`coloors.co` palette file to apply",
        )

        parser.add_argument(
            "--pick",
            metavar="COLORNUM",
            type=int,
            nargs="+",
            help="select and order colors by palette-`COLORNUM`",
        )

        default_add_samples = False
        parser.add_argument(
            "--add-samples",
            action="store_false" if default_add_samples else "store_true",
            default=default_add_samples,
            help=f"add color samples (default: {default_add_samples})",
        )

        group_names = ", ".join([f"`{x.group_name}`" for x in ColorGroup.items()])
        parser.add_argument(
            "--group-color",
            metavar="GROUP=COLOR",
            nargs="+",
            help=f"paint `GROUP` with `COLOR`, where `GROUP` is one of {group_names}",
        )

    # -------------------------------------------------------------------------------

    def handle(self, args):
        """Handle command invocation."""

        if args.palette_file:
            self._load_palette(args)

        for group_color in args.group_color or []:
            name, color = group_color.split("=")
            if (group := ColorGroup.get_by_name(name)) is not None:
                group.set_color(color)

        for i, color_group in enumerate(ColorGroup.items(), start=1):
            if not color_group.ansi:
                continue
            line = " ".join(
                [
                    f".COLOR-{i}",
                    f"{color_group.ansi:16}",
                    "#" + (color_group.rgb or ""),
                    color_group.group_name,
                    color_group.comment or "",
                ]
            )
            print(f"\033[{color_group.ansi}m{line}\033[0m", file=sys.stderr)
            if args.add_samples:
                print(line)

        group_color = None
        # print("#", args.dir_colors)
        for line in args.dir_colors.read_text(args.encoding).splitlines():

            rstripped = line.rstrip()
            group_color = ColorGroup.get_by_comment(rstripped, group_color)

            stripped = rstripped.lstrip()
            if not stripped or stripped[0] == "#":
                print(rstripped)
                continue

            words = stripped.split(maxsplit=2)
            keyword = words[0]
            comment = words[2] if len(words) == 3 else None
            color = ColorGroup.get_by_name(keyword, group_color)

            if not color or not color.ansi:
                print(rstripped)
                continue

            parts = [keyword, color.ansi]
            if color.rgb:
                parts.append("#" + color.rgb)
            if comment:
                parts.append(comment)
            print(" ".join(parts))

    # -------------------------------------------------------------------------------

    def _load_palette(self, args):

        rgb_colors = self._read_palette(args)
        if len(rgb_colors) < len(ColorGroup.items()):
            raise RuntimeError(
                f"Need {len(ColorGroup.items())} colors; "
                f"palette {str(args.palette_file)!r} has only {len(rgb_colors)}."
            )

        if args.pick:
            rgb_colors = [rgb_colors[i - 1] for i in args.pick]

        for color_group, rgb in zip(ColorGroup.items(), rgb_colors):
            color_group.set_color(rgb)

    # -------------------------------------------------------------------------------

    @staticmethod
    def _read_palette(args):
        """Parse `coolors.co` palette file and return list of colors.

        It's all in the first line; e.g. 3 colors
            `/* Coolors Exported Palette - https://coolors.co/00111c-001523-001a2c */`
        """

        if args.palette_num is not None:
            args.palette_file = args.palettes_dir / f"palette ({args.palette_num}).txt"

        palette = args.palette_file.read_text(args.encoding)
        lines = palette.splitlines()
        line = lines[0]

        prefix = "/* Coolors Exported Palette - https://coolors.co/"
        if not line.startswith(prefix):
            raise RuntimeError(f"Invalid prefix in palette `{str(args.palette_file)}`")

        suffix = " */"
        if not line.endswith(suffix):
            raise RuntimeError(f"Invalid suffix in palette `{str(args.palette_file)}`")

        clrs = [x.upper() for x in line[len(prefix) : -len(suffix)].split("-")]
        print("#", line[3:-2])
        return clrs