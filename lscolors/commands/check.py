"""lscolors `check` command."""

from lscolors.commands.basecmd import BaseCommand
from lscolors.commands.utils import colors as color_utils
from lscolors.commands.utils import config as config_utils


class Command(BaseCommand):
    """lscolors `check` command."""

    def __init__(self):
        """Initialize lscolors `check` command."""

        parser = self.add_parser(
            "check",
            help="check database for required items",
            description="Check database in `$LS_COLORS` for required items.",
            epilog="Exit Status: zero indicates success, nonzero indicates failure.",
        )

        parser.set_defaults(cmd=self.handle, prog="lscolors check")
        config_utils.add_arguments(parser)
        color_utils.add_arguments(parser)

    @staticmethod
    def handle(args):
        """Handle command invocation."""

        config, meta_config = config_utils.load(args)

        try:
            colors, meta_colors = color_utils.load(args)
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
