"""lscolors `chart` command."""

from lscolors.commands.base import BaseCommand


class Command(BaseCommand):
    """lscolors `chart` command."""

    def __init__(self):
        """Initialize lscolors `chart` command."""

        parser = self.add_parser(
            "chart",
            formatter_class=self.formatter_class,
            help="print color chart",
            description="Print color-chart.",
        )

        parser.set_defaults(cmd=self.handle, prog="lscolors chart")

        parser.add_argument(
            "color",
            nargs="*",
            help="print color palette with given colors",
        )

    def handle(self, args):
        """Handle command invocation."""

        if args.color:
            self._print_palette(args)
            return

        self._chart_36x6_grey()
        # self._chart2()
        # self._chart_6_squares()
        # self._chart_216_lines()

    @staticmethod
    def _print_palette(args):
        for i in range(1, 4):
            for color in args.color:
                for _ in range(i):
                    text = "Lots of long sample text lorem ipsum dolar sit amet"
                    print(f"\033[{color}m{text} {color}\033[0m")

    @staticmethod
    def _chart_36x6_grey():
        offset = 16
        nlines, ncols = 36, 7
        maxcolor = 255  # nlines * ncols + offset - 1

        for i in range(nlines):
            line = ""
            for j in range(ncols):
                color = offset + (j * nlines) + i
                if color > maxcolor:
                    break
                ansi = f"38;05;{color:03}"
                if j > 0:
                    line += "    "
                line += f"\033[{ansi}m{ansi}\033[0m"
            print(line)

    @staticmethod
    def _chart2():
        for attr in range(8):
            line = ""
            for color in range(8):
                ansi = f"{attr:02};{color + 30:03}"
                if color > 0:
                    line += "    "
                line += f"[{ansi}m{ansi}[0m"
            print(line)

    @staticmethod
    def _chart_6_squares():
        def _6_squares():
            squares = [[], [], [], [], [], []]
            j = 0
            for i in range(216):
                if i > 0 and (i % 6) == 0:
                    j = (j + 1) % 6
                squares[j].append(16 + i)
            return squares

        for square in _6_squares():
            # print(square)
            for ansi in [f"38;05;{color:03}" for color in square]:
                print(f"\033[{ansi}m{ansi}\033[0m")

    @staticmethod
    def _chart_216_lines():
        # /usr/share/vim/vim81/syntax/dircolors.vim
        xterm_palette = ["00", "5f", "87", "af", "d7", "ff"]
        color = 16

        for red in xterm_palette:
            for green in xterm_palette:
                for blue in xterm_palette:
                    ansi = f"38;05;{color:03}"
                    print(f"\033[{ansi}m{color:03} = {ansi} #{red}{green}{blue}\033[0m")
                    color += 1  # noqa