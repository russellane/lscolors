"""AnsiHelpFormatter."""

import argparse
import gettext
import textwrap
from functools import partial

from colors.colors import color

# from icecream import ic, install
# install()
# ic.configureOutput(includeContext=True)

# see /usr/lib/python3.8/argparse.py
# -------------------------------------------------------------------------------


class Colors:
    """Colors."""

    # pylint: disable=too-few-public-methods

    # from https://ethanschoonover.com/solarized/
    #                    SOLARIZED HEX     16/8 TERMCOL  XTERM/HEX
    #                    --------- ------- ---- -------  -----------
    # fmt: off
    brblack = 234   # base03    #002b36  8/4 brblack  234 #1c1c1c
    black = 235     # base02    #073642  0/4 black    235 #262626
    brgreen = 240   # base01    #586e75 10/7 brgreen  240 #585858
    bryellow = 241  # base00    #657b83 11/7 bryellow 241 #626262
    brblue = 244    # base0     #839496 12/6 brblue   244 #808080
    brcyan = 245    # base1     #93a1a1 14/4 brcyan   245 #8a8a8a
    white = 254     # base2     #eee8d5  7/7 white    254 #e4e4e4
    brwhite = 230   # base3     #fdf6e3 15/7 brwhite  230 #ffffd7
    yellow = 136    # yellow    #b58900  3/3 yellow   136 #af8700
    brred = 166     # orange    #cb4b16  9/3 brred    166 #d75f00
    red = 160       # red       #dc322f  1/1 red      160 #d70000
    magenta = 125   # magenta   #d33682  5/5 magenta  125 #af005f
    brmagenta = 61  # violet    #6c71c4 13/5 brmagenta 61 #5f5faf
    blue = 33       # blue      #268bd2  4/4 blue      33 #0087ff
    cyan = 37       # cyan      #2aa198  6/6 cyan      37 #00afaf
    green = 64      # green     #859900  2/2 green     64 #5f8700
    aqua = 43
    # fmt: on

    #   for i in [
    #       brblack,
    #       black,
    #       brgreen,
    #       bryellow,
    #       brblue,
    #       brcyan,
    #       white,
    #       brwhite,
    #       yellow,
    #       brred,
    #       red,
    #       magenta,
    #       brmagenta,
    #       blue,
    #       cyan,
    #       green,
    #       aqua,
    #   ]:
    #       print(color(f"This line is {i}", fg=i))

    # action = partial(color, fg=brred)
    # metavar = partial(color, fg=yellow, style="bold+italic")

    metavar = partial(color, fg=brred, style="italic")
    section = partial(color, fg=blue, style="underline")
    action = partial(color, fg=aqua)
    command_action = partial(color, fg=aqua)
    choices = partial(color, fg=yellow, style="italic")  # command_action
    invalid_choice = partial(color, fg=red, style="italic")


# -------------------------------------------------------------------------------


class AnsiHelpFormatter(argparse.HelpFormatter):
    """AnsiHelpFormatter."""

    def __init__(self, *args, **kwargs):
        """AnsiHelpFormatter."""
        kwargs["width"] = 89
        super().__init__(*args, **kwargs)
        self._is_new_section = None
        self._current_subparser_action = None

    def _add_item(self, func, args):
        """See /usr/lib/python3.8/argparse.py."""
        # fyi: func is _format_usage
        # called first with args: (None, [], [], '')
        if isinstance(args, tuple):
            actions = args[1]  # line 265: args = usage, actions, groups, prefix
            for action in actions:
                # pylint: disable=protected-access
                if isinstance(action, argparse._SubParsersAction):
                    # assert action.dest == "command"
                    # assert action.metavar == "COMMAND"
                    self._current_subparser_action = action
        super()._add_item(func, args)

    # def _format_usage(self, usage, actions, groups, prefix):
    #     """See /usr/lib/python3.8/argparse.py."""
    #     string = super()._format_usage(usage, actions, groups, prefix)
    #     return string

    # def format_help(self):
    #     """See /usr/lib/python3.8/argparse.py."""
    # This is called by `argparse.print_help` in response to `--help`,
    # or perhaps directly by user `print(format_help())`.
    #
    # Prior to that call, however, this will be called by `argparse.add_subparsers`
    # when it is called without passing `prog`, to then extract prog from the result
    # to use as the default.
    #     return super().format_help()

    # -------------------------------------------------------------------------------

    # def add_argument(self, action):
    #     """Override."""
    # ylint: disable=protected-access
    #     return super().add_argument(action)

    def _metavar_formatter(self, action, default_metavar):
        if action.metavar is not None:
            result = Colors.metavar(action.metavar)
        elif action.choices is not None:
            result = ",".join([Colors.metavar(choice) for choice in action.choices])
        else:
            result = Colors.metavar(default_metavar)

        def format(tuple_size):  # pylint: disable=redefined-builtin
            if isinstance(result, tuple):
                return result
            return (result,) * tuple_size

        #
        return format

    def start_section(self, heading):
        """See /usr/lib/python3.8/argparse.py."""
        super().start_section(Colors.section(heading))
        self._is_new_section = True

    # def add_text(self, text):
    #     """See /usr/lib/python3.8/argparse.py."""
    #     super().add_text(text)

    # -------------------------------------------------------------------------------

    def _format_action(self, action):
        """See /usr/lib/python3.8/argparse.py."""

        # ic(action)
        # orig = super()._format_action(action)
        # ic(orig)

        # if action.dest == "command":
        if self._current_subparser_action and action.dest == self._current_subparser_action.dest:
            return self._format_command_action(action)

        # print(f"action.default={action.default}", flush=True)
        if action.dest == "version":  # noqa: SIM114 Use logical or
            # version, new in 3.8, is suppressed by default.
            action.default = None

        elif action.dest == "help":
            # fix this - should not be necessary and incorrectly displays
            # what may have been intentionally hidden.
            action.default = None

        elif action.default == argparse.SUPPRESS:
            # print(f"suppressing {action.dest}", flush=True)
            return ""

        invocation = self._format_action_invocation(action)

        if action.help:
            description = self._expand_help(action)
            description = textwrap.fill(
                self._whitespace_matcher.sub(" ", description).strip(),
                self._width,
                initial_indent="",
                subsequent_indent=" " * (self._action_max_length + 2),
            )

        return (
            "  "
            + Colors.action(invocation)
            + " " * (self._action_max_length - len(invocation))
            + str(self._expand_help(action) if action.help else "")
            + "\n"
        )

    # -------------------------------------------------------------------------------

    def _format_command_action(self, action):
        """New method; not in argparse."""

        lines = [" " * self._current_indent + Colors.metavar(action.metavar)]

        for name, parser in action.choices.items():
            if (description := parser.description) is None:
                continue

            description = textwrap.fill(
                self._whitespace_matcher.sub(" ", description).strip(),
                self._width,
                initial_indent="",
                subsequent_indent=" " * (self._action_max_length + 2),
            )

            gutter = " " * (self._action_max_length - len(name))
            lines.append(f"  {Colors.command_action(name)}{gutter}{description}")

        return str("\n".join(lines) + "\n\n") if len(lines) > 1 else ""


# -------------------------------------------------------------------------------


class AnsiArgumentParser:
    """See /usr/lib/python3.8/argparse.py."""

    # pylint: disable=too-few-public-methods

    @staticmethod
    def _check_value(action, value):

        # converted value must be one of the choices (if specified)
        if action.choices is not None and value not in action.choices:

            msg = gettext.gettext("invalid choice: {} (choose from {})")
            quote = "'"
            #
            value = quote + Colors.invalid_choice(value) + quote
            #
            colored = [Colors.choices(x) for x in action.choices]
            quoted = [quote + x + quote for x in colored]
            choices = ", ".join(quoted)
            #
            raise argparse.ArgumentError(action, msg.format(value, choices))
