	LSCOLORS-REPORT(1)                    User commands                    LSCOLORS-REPORT(1)

#### Description

### Usage

```
lscolors report [-h] [--left | --right] [DIR_COLORS]
```

### Description

Print colorized report for database in `$LS_COLORS`.

### positional arguments:
| option | description |
|:------ |:----------- |
| `DIR_COLORS` | read file `DIR_COLORS` instead of `$LS_COLORS` |

### optional arguments:
| `-h, --help` | show this help message and exit |
| `--left` | format report for display in left window |
| `--right` | format report for display in right window |

### Epilog

A default format is produced when `--left/--right` is not given.

##### See Also

[lscolors-chart](chart.md), [lscolors-check](check.md), [lscolors-configs](configs.md), [lscolors-docs](docs.md), [lscolors-samples](samples.md), [lscolors-sort](sort.md), [lscolors-help](help.md).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]
