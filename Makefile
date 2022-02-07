PACKAGE := lscolors
BUILD += docs
include Python.mk

#-------------------------------------------------------------------------------

MKDOCS := COLUMNS=50 $(PYTHON) -m $(PACKAGE) docs --force
.PHONY:	docs
docs:
	ARGPARSE_COLOR=never $(MKDOCS) docs/txt >README.txt
	ARGPARSE_COLOR=always $(MKDOCS) docs/ansi >README.ansi

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
