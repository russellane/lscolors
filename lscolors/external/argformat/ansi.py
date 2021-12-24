"""AnsiHelpFormatter."""

import argparse
import gettext
import re
from functools import partial

import icecream
from colors.colors import ansilen
from colors.colors import color
from icecream import ic

icecream.install()
ic.configureOutput(prefix="\nic ===> ", includeContext=True)

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
    action = partial(color, fg=red)
    command_action = partial(color, fg=aqua)
    choices = command_action
    option = partial(color, fg=aqua, style="underline")
    normal = partial(color, fg=white)
    backtick = partial(color, fg=yellow, style="italic")
    invalid_choice = partial(color, fg=red, style="italic")

    _re_backtick = None

    # -------------------------------------------------------------------------------

    @classmethod
    def colorize(cls, string):
        """Colorize things in `string`."""

        if cls._re_backtick is None:
            # see ~/dev/pygments/pygments/lexers/markup.py
            # italics fenced by '`'
            cls._re_backtick = re.compile(r"([^`]?)(`[^` \n][^`\n]*`)")

        return re.sub(
            cls._re_backtick,
            lambda m: cls.backtick(m.group(0)),
            string,
        )


# -------------------------------------------------------------------------------


class AnsiHelpFormatter(argparse.HelpFormatter):
    """AnsiHelpFormatter."""

    def __init__(self, *args, **kwargs):
        """AnsiHelpFormatter."""
        # kwargs["width"] = 89
        # kwargs["max_help_position"] = 48  # 24
        super().__init__(*args, **kwargs)
        self._is_new_section = None
        self._current_subparser_action = None
        self._re_ansi = None
        self._is_color_disabled = 0

    #   def _add_item(self, func, args):
    #       """See /usr/lib/python3.8/argparse.py."""
    #       # fyi: func is _format_usage
    #       # called first with args: (None, [], [], '')
    #       if isinstance(args, tuple):
    #           actions = args[1]  # line 265: args = usage, actions, groups, prefix
    #           for action in actions:
    #               # ylint: disable=protected-access
    #               if isinstance(action, argparse._SubParsersAction):
    #                   # assert action.dest == "command"
    #                   # assert action.metavar == "COMMAND"
    #                   self._current_subparser_action = action
    #       super()._add_item(func, args)

    # def _format_usage(self, usage, actions, groups, prefix):
    #     """See /usr/lib/python3.8/argparse.py."""
    #     string = super()._format_usage(usage, actions, groups, prefix)
    #     return string

    def _format_usage(self, usage, actions, groups, prefix):
        # pylint: disable=consider-using-f-string
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements
        _ = gettext.gettext

        if prefix is None:
            prefix = _("usage: ")
        # ic(prefix)

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)
            # ic(usage)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = "%(prog)s" % dict(prog=self._prog)
            # ic(usage)

        # if optionals and positionals are available, calculate usage
        elif usage is None:
            prog = "%(prog)s" % dict(prog=self._prog)
            # ic(usage)

            # split optionals from positionals
            optionals = []
            positionals = []
            for action in actions:
                if action.option_strings:
                    optionals.append(action)
                else:
                    positionals.append(action)

            # build full usage string - colored
            format = self._format_actions_usage  # pylint: disable=redefined-builtin
            action_usage = format(optionals + positionals, groups)
            colored_usage = " ".join([s for s in [prog, action_usage] if s])
            # ic(colored_usage)

            # build full usage string - non-colored
            self._is_color_disabled += 1
            action_usage = format(optionals + positionals, groups)
            self._is_color_disabled -= 1
            usage = " ".join([s for s in [prog, action_usage] if s])
            # ic(usage)

            # wrap the usage parts if it's too long
            text_width = self._width - self._current_indent
            # ic(text_width)
            if len(prefix) + len(usage) > text_width:

                # break usage into wrappable parts
                # pylint: disable=implicit-str-concat
                part_regexp = r"\(.*?\)+(?=\s|$)|" r"\[.*?\]+(?=\s|$)|" r"\S+"
                self._is_color_disabled += 1
                opt_usage = format(optionals, groups)
                # ic(opt_usage)
                pos_usage = format(positionals, groups)
                # ic(pos_usage)
                self._is_color_disabled -= 1
                opt_parts = re.findall(part_regexp, opt_usage)
                # ic(opt_parts)
                pos_parts = re.findall(part_regexp, pos_usage)
                # ic(pos_parts)
                assert " ".join(opt_parts) == opt_usage
                assert " ".join(pos_parts) == pos_usage

                # helper for wrapping lines
                def get_lines(parts, indent, prefix=None):
                    lines = []
                    line = []
                    if prefix is not None:
                        line_len = len(prefix) - 1
                    else:
                        line_len = len(indent) - 1
                    for part in parts:
                        if line_len + 1 + len(part) > text_width and line:
                            lines.append(indent + " ".join(line))
                            line = []
                            line_len = len(indent) - 1
                        line.append(part)
                        line_len += len(part) + 1
                    if line:
                        lines.append(indent + " ".join(line))
                    if prefix is not None:
                        lines[0] = lines[0][len(indent) :]
                    return lines

                # if prog is short, follow it with optionals or positionals
                if len(prefix) + len(prog) <= 0.75 * text_width:
                    indent = " " * (len(prefix) + len(prog) + 1)
                    if opt_parts:
                        lines = get_lines([prog] + opt_parts, indent, prefix)
                        lines.extend(get_lines(pos_parts, indent))
                    elif pos_parts:
                        lines = get_lines([prog] + pos_parts, indent, prefix)
                    else:
                        lines = [prog]

                # if prog is long, put it on its own line
                else:
                    indent = " " * len(prefix)
                    parts = opt_parts + pos_parts
                    lines = get_lines(parts, indent)
                    if len(lines) > 1:
                        lines = []
                        lines.extend(get_lines(opt_parts, indent))
                        lines.extend(get_lines(pos_parts, indent))
                    lines = [prog] + lines

                # join lines into usage
                usage = "\n".join(lines)

            # endif wrap the usage parts if it's too long
            # ic(usage)

            if "\n" not in usage:
                usage = colored_usage
            else:
                lines = usage.splitlines()
                # ic(lines)
                # breakpoint()
                # if self._re_ansi is None:
                #    self._re_ansi = re.compile("\x1b\\[(K|.*?m)")

                cchars = list(colored_usage)
                # ic(cchars)

                usage = ""
                for line in lines:
                    length = len(line)

                    if line and line[0] == " ":
                        while line and line[0] == " ":
                            usage += " "
                            line = line[1:]
                            length -= 1
                        cchars.pop(0)

                    while length:
                        char = cchars.pop(0)
                        if char == "\x1b":
                            usage += char
                            while cchars and (char := cchars.pop(0)) != "m":
                                usage += char
                            usage += char
                        elif char == " ":
                            usage += " "
                            length -= 1
                        else:
                            usage += char
                            length -= 1
                    usage += "\n"
                usage = usage.rstrip()

        # prefix with 'usage:'
        return "%s%s\n\n" % (prefix, usage)

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

    def add_argument(self, action):
        """Docstring."""

        if action.help is not argparse.SUPPRESS:

            # find all invocations
            # self._is_color_disabled += 1
            get_invocation = self._format_action_invocation
            invocations = [get_invocation(action)]
            for subaction in self._iter_indented_subactions(action):
                invocations.append(get_invocation(subaction))
            # self._is_color_disabled -= 1
            ic(invocations)

            # update the maximum item length
            # invocation_length = max([ic(len(s)) for s in invocations])
            invocation_length = max([ic(ansilen(s)) for s in invocations])
            action_length = invocation_length + self._current_indent
            self._action_max_length = ic(max(self._action_max_length, action_length))

            # add the item to the list
            self._add_item(self._format_action, [action])

    def _format_action_invocation(self, action):
        # pylint: disable=no-else-return
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend([Colors.option(x) for x in action.option_strings])

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = ic(self._format_args(action, default))
                for option_string in action.option_strings:
                    ic(option_string)
                    # pylint: disable=consider-using-f-string
                    parts.append("%s %s" % (option_string, args_string))

            return ", ".join(parts)

    def _metavar_formatter(self, action, default_metavar):

        if self._is_color_disabled:
            return super()._metavar_formatter(action, default_metavar)

        if action.metavar is not None:
            result = Colors.metavar(action.metavar)
        elif action.choices is not None:
            # result = ",".join([Colors.metavar(choice) for choice in action.choices])
            result = (
                Colors.normal("{")
                + ",".join([Colors.metavar(choice) for choice in action.choices])
                + Colors.normal("}")
            )
            # choice_strs = [Colors.metavar(choice) for choice in action.choices]
            # result = '{%s}' % ','.join(choice_strs)
        else:
            result = Colors.metavar(default_metavar)

        def format(tuple_size):  # pylint: disable=redefined-builtin
            if isinstance(result, tuple):
                return result
            return (result,) * tuple_size

        #
        return format

    def _add_item(self, func, args):
        """See /usr/lib/python3.8/argparse.py."""
        if isinstance(args, list) and len(args) > 0 and isinstance(args[0], str):
            args = ic([Colors.colorize(x) for x in args])
        super()._add_item(func, args)

    def start_section(self, heading):
        """See /usr/lib/python3.8/argparse.py."""
        super().start_section(Colors.section(heading))
        self._is_new_section = True

    # def add_text(self, text):
    #     """See /usr/lib/python3.8/argparse.py."""
    #     super().add_text(text)
    #     super().add_text(self.colorize(text))

    #   def _bobo__format_action(self, action):
    #       """See /usr/lib/python3.8/argparse.py."""
    #       # if action.dest == "command":
    #       if self._current_subparser_action and action.dest \
    #           == self._current_subparser_action.dest:
    #           return self._format_command_action(action)
    #       # print(f"action.default={action.default}", flush=True)
    #       if action.dest == "version":  # noqa: SIM114 Use logical or
    #           # version, new in 3.8, is suppressed by default.
    #           action.default = None
    #       elif action.dest == "help":
    #           # fix this - should not be necessary and incorrectly displays
    #           # what may have been intentionally hidden.
    #           action.default = None
    #       elif action.default == argparse.SUPPRESS:
    #           # print(f"suppressing {action.dest}", flush=True)
    #           return ""

    # -------------------------------------------------------------------------------

    def _format_action(self, action):
        # pylint: disable=too-many-locals
        # pylint: disable=consider-using-f-string

        # determine the required width and the entry label
        help_position = ic(min(self._action_max_length + 2, self._max_help_position))
        help_width = ic(max(self._width - help_position, 11))
        action_width = ic(help_position - self._current_indent - 2)

        # good? self._is_color_disabled += 1
        # good? action_header = self._format_action_invocation(action)
        # good? ic(action_header)
        # good? len_action_header = len(action_header)
        # good? self._is_color_disabled -= 1
        # good? # action_header = Colors.action(self._format_action_invocation(action))
        # good? action_header = self._format_action_invocation(action)
        # good? ic(action_header)

        action_header = ic(self._format_action_invocation(action))
        len_action_header = ic(ansilen(action_header))

        # no help; start on same line and add a final newline
        if not action.help:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup

        # short action name; start on the same line and pad two spaces
        elif len_action_header <= action_width:
            # orig: tup = self._current_indent, '', action_width, action_header
            # orig: action_header = '%*s%-*s  ' % tup
            indent = " " * self._current_indent
            gutter = " " * (action_width - len_action_header)
            action_header = indent + action_header + gutter + "  "
            indent_first = 0

        # long action name; start on the next line
        else:
            tup = self._current_indent, "", action_header
            action_header = "%*s%s\n" % tup
            indent_first = help_position

        # collect the pieces of the action help
        parts = [action_header]

        # if there was help for the action, add lines of help text
        if action.help:
            help_text = self._expand_help(action)
            help_lines = self._split_lines(help_text, help_width)
            help_lines = [Colors.colorize(x) for x in help_lines]
            parts.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            for line in help_lines[1:]:
                parts.append("%*s%s\n" % (help_position, "", line))

        # or add a newline if the description doesn't end with one
        elif not action_header.endswith("\n"):
            parts.append("\n")

        # if there are any sub-actions, add their help as well
        for subaction in self._iter_indented_subactions(action):
            parts.append(self._format_action(subaction))

        # return a single string
        return self._join_parts(parts)


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

    #-------------------------------------------------------------------------------

    def format_help(self):
        formatter = self._get_formatter()

        # usage
        formatter.add_usage(self.usage, self._actions,
                            self._mutually_exclusive_groups)

        # description
        formatter.add_text(ic(Colors.colorize(self.description)))

        # positionals, optionals and user-defined groups
        for action_group in self._action_groups:
            formatter.start_section(action_group.title)
            formatter.add_text(action_group.description)
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # epilog
        formatter.add_text(Colors.colorize(self.epilog))

        # determine help from format above
        return formatter.format_help()

    def print_usage(self, file=None):
        raise RuntimeError
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        raise RuntimeError
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = _sys.stderr
            file.write(message)


# -------------------------------------------------------------------------------
# class AnsiSection:
#     """Docstring."""
#     # def __init__(self, *args, **kwargs):
#     #     """Docstring."""
#     #     super().__init__(*args, **kwargs)
#     def format_help(self):
#         """Docstring."""
#         ic(self)
#         return super().format_help()
