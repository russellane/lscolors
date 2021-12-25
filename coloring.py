"""Coloring."""

from colors.colors import color

class SolarizedDark:
    """An implementation of https://ethanschoonover.com/solarized/."""

    BASE03  = '#002b36' # noqa
    BASE02  = '#073642' # noqa
    BASE01  = '#586e75' # noqa
    BASE00  = '#657b83' # noqa
    BASE0   = '#839496' # noqa
    BASE1   = '#93a1a1' # noqa
    BASE2   = '#eee8d5' # noqa
    BASE3   = '#fdf6e3' # noqa
    YELLOW  = '#b58900' # noqa
    ORANGE  = '#cb4b16' # noqa
    RED     = '#dc322f' # noqa
    MAGENTA = '#d33682' # noqa
    VIOLET  = '#6c71c4' # noqa
    BLUE    = '#268bd2' # noqa
    CYAN    = '#2aa198' # noqa
    GREEN   = '#859900' # noqa
    WHITE   = BASE0

    NAMES = {
        BASE03:     "BASE03",   # noqa
        BASE02:     "BASE02",   # noqa
        BASE01:     "BASE01",   # noqa
        BASE00:     "BASE00",   # noqa
        BASE0:      "BASE0",    # noqa
        BASE1:      "BASE1",    # noqa
        BASE2:      "BASE2",    # noqa
        BASE3:      "BASE3",    # noqa
        YELLOW:     "YELLOW",   # noqa
        ORANGE:     "ORANGE",   # noqa
        RED:        "RED",      # noqa
        MAGENTA:    "MAGENTA",  # noqa
        VIOLET:     "VIOLET",   # noqa
        BLUE:       "BLUE",     # noqa
        CYAN:       "CYAN",     # noqa
        GREEN:      "GREEN",    # noqa
    }

    #for c in (BASE03, BASE02, BASE01, BASE00, BASE0, BASE1, BASE2, BASE3,
    #          YELLOW, ORANGE, RED, MAGENTA, VIOLET, BLUE, CYAN, GREEN):
    #    print(color(f"This is color {c} {NAMES[c]}", fg=c))
