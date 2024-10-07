"""lscolors `sort` command module."""

import sys
from collections import defaultdict

from lscolors.cmd import LscolorsCmd


class LscolorsSortCmd(LscolorsCmd):
    """lscolors `sort` command class."""

    def init_command(self) -> None:
        """Initialize lscolors `sort` command."""

        self.add_subcommand_parser(
            "sort",
            help="sort lines of database file by color",
            description=self.cli.dedent(
                """
                Filter `stdin` to `stdout` sorting lines of a `DIR_COLORS` file
                by color then filetype. Blank lines and comments are unsorted
                and moved to the end.

                """
            ),
        )

    def run(self) -> None:
        """Perform the command."""

        _ = self  # unused

        # parse lines per https://github.com/coreutils/coreutils/blob/master/src/dircolors.c
        # which strips leading spaces, spaces between keyword and arg,
        # and trailing spaces after arg, which may contain spaces.

        lines_by_color = defaultdict(list)

        # save comments and empty lines for end; for modeline.
        comments = []

        for line in sys.stdin:
            line = line.strip()
            if not line or line[0] == "#":
                comments.append(line)
                continue

            arg = line.split(maxsplit=1)[1]  # (keyword, arg)

            if (i := arg.find("#")) >= 0:
                arg = arg[:i].strip()

            colors = []
            for color in arg.split(";"):
                colors.append(f"{int(color):03}")
            color = "-".join(colors)

            lines_by_color[color].append(line)

        for color in sorted(lines_by_color):
            for line in sorted(lines_by_color[color]):
                print(line)

        for line in comments:
            print(line)
