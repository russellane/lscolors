### Usage

```
lscolors [-h] [-V] COMMAND ...
```

### Description

Utilities for `dircolors(1)` and `dir_colors(5)`

### optional arguments:
| option | description |
|:------ |:----------- |
| `-h, --help` | show this help message and exit |
| `-V, --version` | show program's version number and exit |

### Specify one of:
| COMMAND | |
|:--- | --- |
| [`chart`](docs/md/chart.md) | Print color-chart. |
| [`check`](docs/md/check.md) | Check database in `$LS_COLORS` for required items. |
| [`configs`](docs/md/configs.md) | Print path to sample `.lscolors.yml` and `.dircolors` configuration files. |
| [`docs`](docs/md/docs.md) | Create documentation files for this application. |
| [`report`](docs/md/report.md) | Print colorized report for database in `$LS_COLORS`. |
| [`samples`](docs/md/samples.md) | Create directory and populate with sample files, directories, etc., for each item in `$LS_COLORS`, and all required items in configuration file `CONFIG`. |
| [`sort`](docs/md/sort.md) | Filter `stdin` to `stdout` sorting lines of a `DIR_COLORS` file by color then filetype. Blank lines and comments are unsorted and moved to the end. |

### Epilog

See `lscolors COMMAND --help` for help on a specific command.

