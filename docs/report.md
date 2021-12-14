	LSCOLORS(1)                           User commands                           LSCOLORS(1)

#### Synopsis
	lscolors report [-h] [--left | --right] [DIR_COLORS]

#### Description

Print colorized report for database in `$LS_COLORS` to `stdout`.

##### Positional Arguments
	  DIR_COLORS  read file `DIR_COLORS` instead of `$LS_COLORS`

##### Optional Arguments
	  -h, --help  show this help message and exit
	  --left      format report for display in left window
	  --right     format report for display in right window

##### Notes

A default format is produced when `--left/--right` is not given.

##### See Also

[chart](chart), [check](check), [configs](configs), [docs](docs), [samples](samples), [sort](sort), [help](help).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]