"""Argparse help formatting."""

import argparse
import os
import pathlib

import icecream
import mandown.mandown
from icecream import ic

from . import ansi
from . import markdown

icecream.install()
ic.configureOutput(prefix="\nic ===> ", includeContext=True)


class Argformat:
    """Argparse help formatting."""

    # See /usr/lib/python3.8/argparse.py.

    formatter_class = ansi.AnsiHelpFormatter
    formatter_class_ext = ".ansi"

    def __init__(self, parser):
        """Initialize argparse help formatting.

        >>> import argparse
        >>> import argformat
        >>> parser = argparse.ArgumentParser(prog="hello")
        >>> argformat.argformat(parser)
        """

        if "_NO_ARGFORMAT" in os.environ:
            return

        parser.formatter_class = self.formatter_class
        parser._check_value = ansi.AnsiArgumentParser._check_value  # monkey patch

    # pylint: disable=redefined-builtin
    @classmethod
    def configure(cls, format):
        """Configure argparse help formatting."""

        if format == "ansi":
            cls.formatter_class = ansi.AnsiHelpFormatter
            cls.formatter_class_ext = ".ansi"
        elif format == "md":
            cls.formatter_class = markdown.MarkdownHelpFormatter
            cls.formatter_class_ext = ".md"
        else:
            cls.formatter_class = argparse.HelpFormatter
            cls.formatter_class_ext = ".txt"

    @classmethod
    def print_main_page(cls, main_parser):
        """Print main help page to `stdout`."""

        main_parser.formatter_class = cls.formatter_class
        print(main_parser.format_help())

    @classmethod
    def write_command_pages(cls, main_parser, directory):
        """Create separate help pages for each command in `directory`."""

        also = cls._see_also(main_parser)

        # pylint: disable=protected-access
        for action in main_parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, parser in action.choices.items():

                    parser.formatter_class = cls.formatter_class
                    helpdoc = parser.format_help()

                    if cls.formatter_class == markdown.MarkdownHelpFormatter:
                        lines = helpdoc.splitlines()
                        see_also = ", ".join([v for k, v in also.items() if k != name]) + "."
                        mdoc = mandown.mandown.Mandown(
                            lines, name=f"lscolors-{name}", see_also=see_also
                        )
                        helpdoc = mdoc.render_markdown() + "\n"

                    pathlib.Path(directory, name + cls.formatter_class_ext).write_text(
                        helpdoc, encoding="utf-8"
                    )

    @staticmethod
    def _see_also(main_parser):
        """Docstring."""

        also = {}

        # pylint: disable=protected-access
        for action in main_parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name in action.choices:
                    also[name] = f"[lscolors-{name}]({name}.md)"

        return also


# -------------------------------------------------------------------------------


def argformat(parser):
    """Docstring."""
    return Argformat(parser)


configure = Argformat.configure
print_main_page = Argformat.print_main_page
write_command_pages = Argformat.write_command_pages
