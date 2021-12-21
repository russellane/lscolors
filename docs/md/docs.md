	LSCOLORS-DOCS(1)                      User commands                      LSCOLORS-DOCS(1)

#### Description

### Usage

```
lscolors docs [-h] [-f] {ansi,md,txt} DIR
```

### Description

Create documentation files for this application.

### positional arguments:
| option | description |
|:------ |:----------- |
| `{ansi,md,txt}` | Output format |
| `DIR` | create directory `DIR`. (default: './docs') |

### optional arguments:
| `-h, --help` | show this help message and exit |
| `-f, --force` | Ok to clobber `DIR` if it exists |

### Epilog

This is an internal command used during the packaging process.

##### See Also

[lscolors-chart](chart.md), [lscolors-check](check.md), [lscolors-configs](configs.md), [lscolors-report](report.md), [lscolors-samples](samples.md), [lscolors-sort](sort.md), [lscolors-help](help.md).

----------------------------------------------------------
[page by [mandown](https://github.com/russellane/mandown)]
