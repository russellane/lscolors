	LSCOLORS(1)                           User commands                           LSCOLORS(1)

#### Synopsis
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

##### See Also

[chart](chart), [check](check), [configs](configs), [docs](docs), [report](report), [sort](sort), [help](help).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]