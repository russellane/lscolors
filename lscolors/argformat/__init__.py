"""Argparse help formatting."""

import argparse
import pathlib

import mandown.mandown

from . import ansi
from . import markdown


class Argformat:
    """Argparse help formatting."""

    FormatterClass = ansi.AnsiHelpFormatter

    def __init__(self, parser):
        """Initialize argparse help formatting.

        >>> import argparse
        >>> import argformat
        >>> parser = argparse.ArgumentParser(prog="hello")
        >>> argformat.argformat(parser)
        """

        parser.formatter_class = self.FormatterClass
        parser._check_value = ansi.AnsiArgumentParser._check_value  # monkey patch

    # pylint: disable=redefined-builtin
    @classmethod
    def configure(cls, format):
        """Configure argparse help formatting."""

        if format == "ansi":
            cls.FormatterClass = ansi.AnsiHelpFormatter
            cls.Extension = ".ansi"
        elif format == "md":
            cls.FormatterClass = markdown.MarkdownHelpFormatter
            cls.Extension = ".md"
        else:
            cls.FormatterClass = argparse.HelpFormatter
            cls.Extension = ".txt"

    @classmethod
    def print_main_page(cls, main_parser):
        """Print main help page to `stdout`."""

        main_parser.formatter_class = cls.FormatterClass
        print(main_parser.format_help())

    @classmethod
    def write_command_pages(cls, main_parser, directory):
        """Create separate help pages for each command in `directory`."""

        also = cls._see_also(main_parser)

        # pylint: disable=protected-access
        for action in main_parser._subparsers._actions:
            if isinstance(action, argparse._SubParsersAction):
                for name, parser in action.choices.items():

                    parser.formatter_class = cls.FormatterClass
                    helpdoc = parser.format_help()

                    if cls.FormatterClass == markdown.MarkdownHelpFormatter:
                        lines = helpdoc.splitlines()
                        see_also = ", ".join([v for k, v in also.items() if k != name]) + "."
                        mdoc = mandown.mandown.Mandown(
                            lines, name=f"lscolors-{name}", see_also=see_also
                        )
                        helpdoc = mdoc.render_markdown() + "\n"

                    pathlib.Path(directory, name + cls.Extension).write_text(
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
