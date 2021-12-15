	LSCOLORS(1)                           User commands                           LSCOLORS(1)

#### Synopsis
	lscolors [-h] [-V] [--bobo [FILE]] COMMAND ...

#### Description

Utilities for `dircolors(1)` and `dir_colors(5)`

##### Optional Arguments
	  -h, --help     show this help message and exit
	  -V, --version  show program's version number and exit
	  --bobo [FILE]  test option for testing

##### Commands
	    chart        print color chart
	    check        check database for required items
	    configs      print path to sample configuration files
	    docs         Create documentation for this application
	    report       print colorized database report
	    samples      create directory of sample filesystem items
	    sort         sort lines of database file by color
	    help         same as `--help`

##### Notes

See `lscolors COMMAND --help` for help on a specific command.

--------------------------------------------------------------------------------

### Lscolors Chart
	lscolors chart [-h]

#### Description

Print color-chart.

##### Optional Arguments
	  -h, --help  show this help message and exit

--------------------------------------------------------------------------------

### Lscolors Check
	lscolors check [-h] [-q] [--config CONFIG] [DIR_COLORS]

#### Description

Check database in `$LS_COLORS` for required items.

##### Positional Arguments
	  DIR_COLORS       read file `DIR_COLORS` instead of `$LS_COLORS`

##### Optional Arguments
	  -h, --help       show this help message and exit
	  -q, --quiet      suppress warning if default `CONFIG` cannot be found
	  --config CONFIG  require filenames, directories and extensions specified in `CONFIG` file.
	                   (default: '.lscolors.yml')

##### Notes

Exit Status: zero indicates success, nonzero indicates failure.

--------------------------------------------------------------------------------

### Lscolors Configs
	lscolors configs [-h]

#### Description

Print path to sample `.lscolors.yml` and `.dircolors` configuration files.

##### Optional Arguments
	  -h, --help  show this help message and exit

--------------------------------------------------------------------------------

### Lscolors Report
	lscolors report [-h] [--left | --right] [DIR_COLORS]

#### Description

Print colorized report for database in `$LS_COLORS`.

##### Positional Arguments
	  DIR_COLORS  read file `DIR_COLORS` instead of `$LS_COLORS`

##### Optional Arguments
	  -h, --help  show this help message and exit
	  --left      format report for display in left window
	  --right     format report for display in right window

##### Notes

A default format is produced when `--left/--right` is not given.

--------------------------------------------------------------------------------

### Lscolors Samples
	lscolors samples [-h] [-q] [--config CONFIG] [--samplesdir DIR] [-f] [DIR_COLORS]

#### Description

Create directory and populate with sample files, directories, etc., for each item in
`$LS_COLORS`, and all required items in configuration file `CONFIG`.

##### Positional Arguments
	  DIR_COLORS        read file `DIR_COLORS` instead of `$LS_COLORS`

##### Optional Arguments
	  -h, --help        show this help message and exit
	  -q, --quiet       suppress warning if default `CONFIG` cannot be found
	  --config CONFIG   require filenames, directories and extensions specified in `CONFIG` file.
	                    (default: '.lscolors.yml')
	  --samplesdir DIR  create directory `DIR`. (default: './lscolors-samples')
	  -f, --force       Ok to clobber `DIR` if it exists

--------------------------------------------------------------------------------

### Lscolors Sort
	lscolors sort [-h]

#### Description

Filter `stdin` to `stdout` sorting lines of a `DIR_COLORS` file by color then filetype. Blank
lines and comments are unsorted and moved to the end.

##### Optional Arguments
	  -h, --help  show this help message and exit

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]
