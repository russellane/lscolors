"""lscolors config."""
# -------------------------------------------------------------------------------

import os

import yaml

_DEFAULT_CONFIG_FILE = ".lscolors.yml"

# -------------------------------------------------------------------------------


def add_arguments(parser):
    """Add arguments to parser."""

    parser.set_defaults(config=_DEFAULT_CONFIG_FILE)

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="suppress warning if default `CONFIG` cannot be found.",
    )

    parser.add_argument(
        "--config",
        help="require filenames, directories and extensions "
        "specified in `CONFIG` file. "
        f"(default: {_DEFAULT_CONFIG_FILE!r})",
    )


# -------------------------------------------------------------------------------


def load(args):
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

    if args.config != _DEFAULT_CONFIG_FILE:
        with open(args.config, encoding="utf-8") as file:
            meta = f"cfg={args.config!r}"
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

    if not args.quiet:
        print(f"{args.prog}: warning; no config file {_DEFAULT_CONFIG_FILE!r}", flush=True)

    return {
        "required_filenames": [],
        "required_directories": [],
        "required_extensions": [],
    }, "<no config>"


# -------------------------------------------------------------------------------
