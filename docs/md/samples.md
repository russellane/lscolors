	LSCOLORS-SAMPLES(1)                   User commands                   LSCOLORS-SAMPLES(1)

#### Description

### Usage

```
lscolors samples [-h] [-q] [--config CONFIG] [--samplesdir DIR] [-f] [DIR_COLORS]
```

### Description

Create directory and populate with sample files, directories, etc., for each item in
`$LS_COLORS`, and all required items in configuration file `CONFIG`.

### positional arguments:
| option | description |
|:------ |:----------- |
| `DIR_COLORS` | read file `DIR_COLORS` instead of `$LS_COLORS` |

### optional arguments:
| `-h, --help` | show this help message and exit |
| `-q, --quiet` | suppress warning if default `CONFIG` cannot be found |
| `--config CONFIG` | require filenames, directories and extensions specified in `CONFIG` file. (default: '.lscolors.yml') |
| `--samplesdir DIR` | create directory `DIR`. (default: './lscolors-samples') |
| `-f, --force` | Ok to clobber `DIR` if it exists |

### Epilog

##### See Also

[lscolors-chart](chart.md), [lscolors-check](check.md), [lscolors-configs](configs.md), [lscolors-docs](docs.md), [lscolors-report](report.md), [lscolors-sort](sort.md), [lscolors-help](help.md).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]
