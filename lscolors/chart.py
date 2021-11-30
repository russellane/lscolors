"""lscolors `chart` command."""


def add_parser(subs):
    """Add command parser."""

    parser = subs.add_parser(
        "chart",
        help="print color chart",
        description="Print color-chart to `stdout`.",
    )

    parser.set_defaults(cmd=_handle, prog="lscolors chart")


def _handle(args):

    _ = args  # unused
    offset = 16
    nlines, ncols = 36, 6
    maxcolor = nlines * ncols + offset - 1

    for i in range(nlines):
        line = ""
        for j in range(ncols):
            color = offset + (j * nlines) + i
            if color > maxcolor:
                break
            ansi = f"38;05;{color:03}"
            if j > 0:
                line += "    "
            line += f"[{ansi}m{ansi}[0m"
        print(line)


def _handle2():

    for square in _six_squares():
        print(square)
        for ansi in [f"38;05;{color:03}" for color in square]:
            print(f"[{ansi}m{ansi}[0m")


def _six_squares():

    squares = [[], [], [], [], [], []]
    j = 0
    for i in range(216):
        if i > 0 and (i % 6) == 0:
            j = (j + 1) % 6
        squares[j].append(16 + i)
    return squares
