"""lscolors `check` command."""

import lscolors.colors
import lscolors.config


def add_parser(subs):
    """Add command parser."""

    parser = subs.add_parser(
        "check",
        help="check database for required items",
        description="Check database in `$LS_COLORS` for required items.",
        epilog="Exit Status: zero indicates success, nonzero indicates failure.",
    )

    parser.set_defaults(cmd=_handle, prog="lscolors check")
    lscolors.config.add_arguments(parser)
    lscolors.colors.add_arguments(parser)


def _handle(args):

    config, meta_config = lscolors.config.load(args)

    try:
        colors, meta_colors = lscolors.colors.load(args)
    except RuntimeError as err:
        raise SyntaxError(
            f"{args.prog}: failure; {err}\n" f"{args.prog}: {meta_config}"
        ) from err

    missing = []
    required = 0
    for item in (
        config["required_filenames"]
        + config["required_directories"]
        + config["required_extensions"]
    ):
        required += 1
        if item not in colors:
            missing.append(item)

    if (nmissing := len(missing)) > 0:
        raise SyntaxError(
            f"{args.prog}: failure; {len(colors)} items; "
            f"{required - nmissing}/{required} required; "
            f"{nmissing} missing {missing}\n"
            f"{args.prog}: {meta_colors}; {meta_config}"
        )

    print(
        f"{args.prog}: success; {len(colors)} items; "
        f"{required}/{required} required.\n"
        f"{args.prog}: {meta_colors}; {meta_config}"
    )
