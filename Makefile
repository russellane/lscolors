PACKAGE := lscolors
BUILD += docs
include Python.mk

#-------------------------------------------------------------------------------

.PHONY:		docs
docs:
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) docs --force >README.md

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
