### Usage

```
lscolors [-h] [-V] [--test-one [***FILE***]] [--test-two [***FILE***]]
         ***COMMAND*** ...
```

### Description

Utilities for `dircolors(1)` and `dir_colors(5)`

### optional arguments:
| option | description |
|:------ |:----------- |
| -h, --help | show this help message and exit |
| -V, --version | show program's version number and exit |
| --test-one [***FILE***] | test option for testing |
| --test-two [***FILE***] | another test option for testing |

### Specify one of:
| <span style="color: darkred">***COMMAND***</span> | |
|:--- | --- |
| `[chart](docs/chart.md)` | Print color-chart. |
| `[check](docs/check.md)` | Check database in `$LS_COLORS` for required items. |
| `[configs](docs/configs.md)` | Print path to sample `.lscolors.yml` and `.dircolors` configuration files. |
| `[docs](docs/docs.md)` | Woohoo. |
| `[report](docs/report.md)` | Print colorized report for database in `$LS_COLORS`. |
| `[samples](docs/samples.md)` | Create directory and populate with sample files, directories, etc., for each item in `$LS_COLORS`, and all required items in configuration file `CONFIG`. |
| `[sort](docs/sort.md)` | Filter `stdin` to `stdout` sorting lines of a `DIR_COLORS` file by color then filetype. Blank lines and comments are unsorted and moved to the end. |

### Epilog

See `lscolors COMMAND --help` for help on a specific command.

