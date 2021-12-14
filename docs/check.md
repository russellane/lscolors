	LSCOLORS-CHECK(1)                     User commands                     LSCOLORS-CHECK(1)

#### Synopsis
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

##### See Also

[lscolors-chart](chart.md), [lscolors-configs](configs.md), [lscolors-docs](docs.md), [lscolors-report](report.md), [lscolors-samples](samples.md), [lscolors-sort](sort.md), [lscolors-help](help.md).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]