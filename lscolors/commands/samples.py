"""lscolors `samples` command."""

import os
import socket
import stat

from lscolors.cmd import LscolorsCmd
from lscolors.commands.utils import colors as colors_utils
from lscolors.commands.utils import config as config_utils
from lscolors.commands.utils import mkdir


class LscolorsSamplesCmd(LscolorsCmd):
    """lscolors `samples` command."""

    def init_command(self) -> None:
        """Initialize lscolors `samples` command."""

        parser = self.add_subcommand_parser(
            "samples",
            help="create directory of sample filesystem items",
            description=self.cli.dedent(
                """
                Create directory and populate with sample files, directories, etc.,
                for each item in `$LS_COLORS`, and all required items in
                configuration file `CONFIG`.
                """
            ),
        )

        self.add_config_option(parser)
        self.add_colors_argument(parser)

        arg = parser.add_argument(
            "--samplesdir",
            metavar="DIR",
            default="./lscolors-samples",
            help="create directory `DIR`",
        )
        self.cli.add_default_to_help(arg)

        parser.add_argument(
            "-f", "--force", action="store_true", help="Ok to clobber `DIR` if it exists"
        )

        #
        self._seqno = 0  # noqa

    def _fname(self, name: str) -> str:
        self._seqno += 1
        return f"{self._seqno:02}-{name}"

    def run(self) -> None:
        """Perform the command."""

        colors, meta_colors = colors_utils.load(self.options)
        config, meta_config = config_utils.load(self.options)

        mkdir.mkdir(self.options.samplesdir, self.options.force)
        print(
            self.options.prog,
            "creating directory",
            repr(self.options.samplesdir),
            "for",
            meta_colors,
            meta_config,
        )

        os.chdir(self.options.samplesdir)
        top = os.getcwd()

        # .../sample-files/colors/x.038-005-213.py
        path = os.path.join(top, "colors")
        os.mkdir(path)
        os.chdir(path)
        self._samples(colors, config, "x.{color}{name}")

        # .../sample-files/names/sample.py
        path = os.path.join(top, "names")
        os.mkdir(path)
        os.chdir(path)
        self._samples(colors, config, "sample{name}")

        # .../sample-files/hybrid/x.py.038-005-213.py
        path = os.path.join(top, "hybrid")
        os.mkdir(path)
        os.chdir(path)
        self._samples(colors, config, "x{name}.{color}{name}")

    def _samples(self, colors: dict[str, str], config: dict[str, list[str]], fmt: str) -> None:

        for name in config["required_filenames"]:
            if name[0] == "*":
                name = name[1:]
                with open(name, mode="w", encoding="utf-8"):
                    pass

        for name in config["required_directories"]:
            os.mkdir(name)

        for name in config["required_extensions"]:
            with open("required" + name, mode="w", encoding="utf-8"):
                pass

        self._create_basic_filetypes()
        self._create_extension_samples(colors, fmt)

        # sprinkle plenty of directory color around
        for alpha in "aiptz":
            os.mkdir(f"required.{alpha}-directory")
        for alpha in [".A", ".z", "A"]:
            os.mkdir(f"{alpha}-directory")

    def _create_basic_filetypes(self) -> None:
        """Create filesystem object for each "basic" filetype.

        Output from `dircolors --print-database`:

            #NORMAL 00 # no color code at all
            #FILE 00 # regular file: use no color at all
            RESET 0 # reset to "normal" color
            DIR 01;34 # directory
            LINK 01;36 # symbolic link. (If you set this to 'target' instead of a
            # numerical value, the color is as for the file pointed to.)
            MULTIHARDLINK 00 # regular file with more than one link
            FIFO 40;33 # pipe
            SOCK 01;35 # socket
            DOOR 01;35 # door
            BLK 40;33;01 # block device driver
            CHR 40;33;01 # character device driver
            ORPHAN 40;31;01 # symlink to nonexistent file, or non-stat'able file ...
            MISSING 00 # ... and the files they point to
            SETUID 37;41 # file that is setuid (u+s)
            SETGID 30;43 # file that is setgid (g+s)
            CAPABILITY 30;41 # file with capability
            STICKY_OTHER_WRITABLE 30;42 # dir that is sticky and other-writable (+t,o+w)
            OTHER_WRITABLE 34;42 # dir that is other-writable (o+w) and not sticky
            STICKY 37;44 # dir with the sticky bit set (+t) and not other-writable
            # This is for files with execute permission:
            EXEC 01;32

        Objects are named for `ls -l` to display in same order as template.
        """

        # pylint: disable=too-many-locals
        # pylint: disable=too-many-statements

        # NORMAL 00 # no color code at all
        normal_text = self._fname("NORMAL")
        with open(normal_text, mode="w", encoding="utf-8"):
            pass

        # FILE 00 # regular file: use no color at all
        regular_file = self._fname("FILE-regular-file")
        with open(regular_file, mode="w", encoding="utf-8"):
            pass

        # RESET 0 # reset to "normal" color
        reset_file = self._fname("RESET")
        with open(reset_file, mode="w", encoding="utf-8"):
            pass

        # DIR 00;36 # directory
        dir_not_ow = self._fname("DIR-not-other-writable")
        os.mkdir(dir_not_ow)

        # LINK 40;33 # symbolic link. (If you set this to 'target' instead of a
        # numerical value, the color is as for the file pointed to.)
        symlink_to_file = self._fname("LINK-symlink-file")
        os.symlink(regular_file, symlink_to_file)

        # MULTIHARDLINK 03 # regular file with more than one link
        hardlink_file1 = self._fname("MULTIHARDLINK-file1")
        with open(hardlink_file1, mode="w", encoding="utf-8"):
            pass

        # FIFO 03;31 # pipe
        fifo = self._fname("FIFO-named-pipe")
        os.mkfifo(fifo)

        # SOCK 03;32 # socket
        sockname = self._fname("SOCK-unix-domain-socket")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(sockname)

        # DOOR 03;32 # door
        door = self._fname("DOOR-fake")
        with open(door, mode="w", encoding="utf-8"):
            pass

        # BLK 40;33;01 # block device driver
        blk_device = self._fname("BLK-block-device")
        try:
            os.mknod(blk_device, stat.S_IFBLK)
        except PermissionError:
            blk_device = blk_device + "-fake"
            with open(blk_device, mode="w", encoding="utf-8"):
                pass

        # CHR 40;33;01 # character device driver
        chr_device = self._fname("CHR-character-device")
        try:
            os.mknod(chr_device, stat.S_IFCHR)
        except PermissionError:
            chr_device = blk_device + "-fake"
            with open(chr_device, mode="w", encoding="utf-8"):
                pass

        # ORPHAN 40;31;03 # symlink to nonexistent file, or non-stat'able file
        symlink_to_orphan = self._fname("ORPHAN")
        os.symlink("nonexistent-file1", symlink_to_orphan)

        # MISSING 03 # ... and the files they point to
        # from `man 5 dir_colors`:
        #       (a nonexistent file which nevertheless
        #        has a symbolic link pointing to it)
        # I don't know what this means or how to create it.
        symlink_to_missing = self._fname("MISSING-fake")
        os.symlink("nonexistent-file2", symlink_to_missing)

        # SETUID 37;41 # file that is setuid (u+s)
        suid_file = self._fname("SETUID-file")
        with open(suid_file, mode="w", encoding="utf-8"):
            pass
        os.chmod(suid_file, stat.S_ISUID | 0o0755)

        # SETGID 30;43 # file that is setgid (g+s)
        sgid_file = self._fname("SETGID-file")
        with open(sgid_file, mode="w", encoding="utf-8"):
            pass
        os.chmod(sgid_file, stat.S_ISGID | 0o0755)

        # CAPABILITY 30;41 # file with capability
        cap_file = self._fname("CAPABILITY-file")
        with open(cap_file, mode="w", encoding="utf-8"):
            pass

        # STICKY_OTHER_WRITABLE 30;42 # dir that is sticky and other-writable (+t,o+w)
        sticky_dir_ow = self._fname("STICKY-dir-other-writable")
        os.mkdir(sticky_dir_ow)
        os.chmod(sticky_dir_ow, stat.S_ISVTX | 0o0777)

        # OTHER_WRITABLE 03;35 # dir that is other-writable (o+w) and not sticky
        dir_ow = self._fname("DIR-other-writable")
        os.mkdir(dir_ow)
        os.chmod(dir_ow, 0o0777)

        # STICKY 37;44 # dir with the sticky bit set (+t) and not other-writable
        sticky_dir = self._fname("STICKY-dir-not-other-writable")
        os.mkdir(sticky_dir)
        os.chmod(sticky_dir, stat.S_ISVTX | 0o0755)

        # EXEC 00 # This is for files with execute permission:
        exec_file = self._fname("EXEC-executable")
        with open(exec_file, mode="w", encoding="utf-8"):
            pass
        os.chmod(exec_file, 0o0755)

        # -- end of template --

        # complete MULTIHARDLINK
        os.link(hardlink_file1, self._fname("MULTIHARDLINK-file2"))

        # symlinks for everyone! set "LINK target" to see...
        os.symlink(symlink_to_file, self._fname("LINK-symlink-to-symlink-to-file"))
        os.symlink(fifo, self._fname("LINK-symlink-to-fifo"))
        os.symlink(sockname, self._fname("LINK-symlink-to-socket"))
        os.symlink(door, self._fname("LINK-symlink-to-door"))
        os.symlink(blk_device, self._fname("LINK-symlink-to-blk_device"))
        os.symlink(chr_device, self._fname("LINK-symlink-to-chr_device"))
        os.symlink(symlink_to_orphan, self._fname("LINK-symlink-to-symlink_to_orphan"))
        os.symlink(symlink_to_missing, self._fname("LINK-symlink-to-symlink_to_missing"))
        os.symlink(suid_file, self._fname("LINK-symlink-to-suid_file"))
        os.symlink(sgid_file, self._fname("LINK-symlink-to-sgid_file"))
        os.symlink(cap_file, self._fname("LINK-symlink-to-cap_file"))
        os.symlink(sticky_dir_ow, self._fname("LINK-symlink-to-sticky_dir_ow"))
        os.symlink(dir_ow, self._fname("LINK-symlink-to-dir_ow"))
        os.symlink(sticky_dir, self._fname("LINK-symlink-to-sticky_dir"))
        os.symlink(exec_file, self._fname("LINK-symlink-to-exec_file"))

    @staticmethod
    def _create_extension_samples(colors: dict[str, str], fmt: str) -> None:

        for name in [
            x
            for x in colors
            if x
            not in [
                "bd",
                "ca",
                "cd",
                "di",
                "do",
                "ex",
                "ln",
                "mh",
                "mi",
                "or",
                "ow",
                "pi",
                "rs",
                "sg",
                "so",
                "st",
                "su",
                "tw",
            ]
        ]:
            color = "-".join([f"{int(x):03}" for x in colors[name].split(";")])
            filename = fmt.format(color=color, name=name)
            try:
                os.stat(filename)
            except FileNotFoundError:
                with open(filename, mode="w", encoding="utf-8"):
                    pass
