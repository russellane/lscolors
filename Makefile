PACKAGE := lscolors
BUILD += docs
include Python.mk

#-------------------------------------------------------------------------------

.PHONY:		docs
docs:
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) --long-help >README.md
		# COLUMNS=97 $(PYTHON) -m $(PACKAGE) docs --force docs/ansi >README.txt

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
