"""lscolors config."""

import os
from argparse import ArgumentParser, Namespace

import yaml
from libcli import BaseCLI

_DEFAULT_CONFIG_FILE = ".lscolors.yml"


def add_config_option(cli: BaseCLI, parser: ArgumentParser) -> None:
    """Add arguments to parser."""

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="suppress warning if default `CONFIG` cannot be found",
    )

    arg = parser.add_argument(
        "--config",
        default=_DEFAULT_CONFIG_FILE,
        help="require filenames, directories and extensions specified in `CONFIG` file",
    )
    cli.add_default_to_help(arg)


def load(options: Namespace) -> tuple[dict[str, list[str]], str]:
    """Load `lscolors` configuration.

    Load the config file given on the command line, if given, or search for a
    default config file in each directory from CWD to HOME or ROOT.

    Return multiple values:
        config: dict {
            required_filenames:
            required_directories:
            required_extensions:
        }
        meta: fully-qualified path of the loaded configuration file.
    """

    if options.config != _DEFAULT_CONFIG_FILE:
        with open(options.config, encoding="utf-8") as file:
            meta = f"cfg={options.config!r}"
            return yaml.load(file.read(), Loader=yaml.BaseLoader), meta

    # search each dir from CWD to HOME or ROOT

    here = os.getcwd()
    home = os.path.expanduser("~")

    while True:
        path = os.path.join(here, _DEFAULT_CONFIG_FILE)
        try:
            with open(path, encoding="utf-8") as file:
                meta = f"cfg={path!r}"
                return yaml.load(file.read(), Loader=yaml.BaseLoader), meta
        except FileNotFoundError:
            if here in (home, os.path.sep):
                break
            here = os.path.dirname(here)

    if not options.quiet:
        print(f"{options.prog}: warning; no config file {_DEFAULT_CONFIG_FILE!r}", flush=True)

    return {
        "required_filenames": [],
        "required_directories": [],
        "required_extensions": [],
    }, "<no config>"
