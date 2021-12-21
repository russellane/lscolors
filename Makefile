PACKAGE := lscolors
BUILD += docs
include Python.mk

#-------------------------------------------------------------------------------

.PHONY:		docs
docs:
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) docs ansi --force docs/ansi >README.ansi
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) docs md --force docs/md >README.md
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) docs txt --force docs/txt >README.txt

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
