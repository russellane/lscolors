	LSCOLORS(1)                           User commands                           LSCOLORS(1)

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

[chart](chart), [configs](configs), [docs](docs), [report](report), [samples](samples), [sort](sort), [help](help).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]