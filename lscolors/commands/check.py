"""lscolors `check` command."""

import lscolors


class Command(lscolors.command.Command):
    """lscolors `check` command."""

    def __init__(self):
        """Initialize lscolors `check` command."""

        super().__init__()

        parser = self.subs.add_parser(
            "check",
            help="check database for required items",
            description="Check database in `$LS_COLORS` for required items.",
            epilog="Exit Status: zero indicates success, nonzero indicates failure.",
        )

        parser.set_defaults(cmd=self.handle, prog="lscolors check")
        lscolors.config.add_arguments(parser)
        lscolors.colors.add_arguments(parser)

    @staticmethod
    def handle(args):
        """Handle command invocation."""

        config, meta_config = lscolors.config.load(args)

        try:
            colors, meta_colors = lscolors.colors.load(args)
        except RuntimeError as err:
            raise RuntimeError(
                f"{args.prog}: failure; {err}\n" f"{args.prog}: {meta_config}"
            ) from err

        required = (
            config["required_filenames"]
            + config["required_directories"]
            + config["required_extensions"]
        )
        nrequired = len(required)
        # missing = [x for x in required if x not in colors]
        missing = []
        for item in required:
            if item not in colors:
                missing.append(item)

        if (nmissing := len(missing)) > 0:
            raise RuntimeError(
                f"{args.prog}: failure; {len(colors)} items; "
                f"{nrequired - nmissing}/{nrequired} required; "
                f"{nmissing} missing {missing}\n"
                f"{args.prog}: {meta_colors}; {meta_config}"
            )

        print(
            f"{args.prog}: success; {len(colors)} items; "
            f"{nrequired}/{nrequired} required.\n"
            f"{args.prog}: {meta_colors}; {meta_config}"
        )
