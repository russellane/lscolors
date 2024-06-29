# lscolors
```
usage: lscolors [-h] [-H] [-v] [-V] [--print-config] [--print-url]
                [--completion [SHELL]]
                COMMAND ...

Utilities for `dircolors(1)` and `dir_colors(5)`.

Specify one of:
  COMMAND
    chart               Print color chart.
    check               Check database for required items.
    configs             Print path to sample configuration files.
    docs                Create documentation.
    paint               Paint dircolors.
    report              Print colorized database report.
    samples             Create directory of sample filesystem items.
    sort                Sort lines of database file by color.

General options:
  -h, --help            Show this help message and exit.
  -H, --long-help       Show help for all commands and exit.
  -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
  -V, --version         Print version number and exit.
  --print-config        Print effective config and exit.
  --print-url           Print project url and exit.
  --completion [SHELL]  Print completion scripts for `SHELL` and exit
                        (default: `bash`).

See `lscolors COMMAND --help` for help on a specific command.
```

## lscolors chart
```
usage: lscolors chart [-h] [color ...]

Print color-chart.

positional arguments:
  color       Print color palette with given colors.

options:
  -h, --help  Show this help message and exit.
```

## lscolors check
```
usage: lscolors check [-h] [-q] [--config CONFIG] [DIR_COLORS]

Check database in `$LS_COLORS` for required items.

positional arguments:
  DIR_COLORS       Read file `DIR_COLORS` instead of `$LS_COLORS`.

options:
  -h, --help       Show this help message and exit.
  -q, --quiet      Suppress warning if default `CONFIG` cannot be found.
  --config CONFIG  Require filenames, directories and extensions specified in
                   `CONFIG` file.

Exit Status: zero indicates success, nonzero indicates failure.
```

## lscolors configs
```
usage: lscolors configs [-h]

Print path to sample `.lscolors.yml` and `.dircolors` configuration files.

options:
  -h, --help  Show this help message and exit.
```

## lscolors docs
```
usage: lscolors docs [-h] [-f] {ansi,md,txt} DIR

Create documentation files for this application.

positional arguments:
  {ansi,md,txt}  Output format.
  DIR            Create directory `DIR`. (default: './docs').

options:
  -h, --help     Show this help message and exit.
  -f, --force    Ok to clobber `DIR` if it exists.

This is an internal command used during the packaging process.
```

## lscolors paint
```
usage: lscolors paint [-h] [--encoding NAME] [--palettes-dir DIR]
                      [--palette-num NUMBER] [--palette-file FILE]
                      [--pick COLORNUM [COLORNUM ...]] [--add-samples]
                      [--group-color GROUP=COLOR [GROUP=COLOR ...]]
                      [DIR_COLORS]

Apply palette to dircolors.

positional arguments:
  DIR_COLORS            Read `DIR_COLORS` file.

options:
  -h, --help            Show this help message and exit.
  --encoding NAME       File encoding.
  --palettes-dir DIR    Directory of `coloors.co` palettes.
  --palette-num NUMBER  Id of `coloors.co` palette file to apply.
  --palette-file FILE   `coloors.co` palette file to apply.
  --pick COLORNUM [COLORNUM ...]
                        Select and order colors by palette-`COLORNUM`.
  --add-samples         Add color samples.
  --group-color GROUP=COLOR [GROUP=COLOR ...]
                        Paint `GROUP` with `COLOR`, where `GROUP` is one of
                        `archive`, `image`, `audio`, `data`, `source`,
                        `config`, `history`, `doc`, `NORMAL`, `FILE`, `RESET`,
                        `DIR`, `LINK`, `MULTIHARDLINK`, `FIFO`, `SOCK`,
                        `DOOR`, `BLK`, `CHR`, `ORPHAN`, `MISSING`, `SETUID`,
                        `SETGID`, `CAPABILITY`, `STICKY_OTHER_WRITABLE`,
                        `OTHER_WRITABLE`, `STICKY`, `EXEC`.
```

## lscolors report
```
usage: lscolors report [-h] [--left | --right] [DIR_COLORS]

Print colorized report for database in `$LS_COLORS`.

positional arguments:
  DIR_COLORS  Read file `DIR_COLORS` instead of `$LS_COLORS`.

options:
  -h, --help  Show this help message and exit.
  --left      Format report for display in left window.
  --right     Format report for display in right window.

A default format is produced when `--left/--right` is not given.
```

## lscolors samples
```
usage: lscolors samples [-h] [-q] [--config CONFIG] [--samplesdir DIR] [-f]
                        [DIR_COLORS]

Create directory and populate with sample files, directories, etc.,
for each item in `$LS_COLORS`, and all required items in
configuration file `CONFIG`.

positional arguments:
  DIR_COLORS        Read file `DIR_COLORS` instead of `$LS_COLORS`.

options:
  -h, --help        Show this help message and exit.
  -q, --quiet       Suppress warning if default `CONFIG` cannot be found.
  --config CONFIG   Require filenames, directories and extensions specified in
                    `CONFIG` file.
  --samplesdir DIR  Create directory `DIR`.
  -f, --force       Ok to clobber `DIR` if it exists.
```

## lscolors sort
```
usage: lscolors sort [-h]

Filter `stdin` to `stdout` sorting lines of a `DIR_COLORS` file
by color then filetype. Blank lines and comments are unsorted
and moved to the end.

options:
  -h, --help  Show this help message and exit.
```

