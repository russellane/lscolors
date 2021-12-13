PACKAGE := lscolors
BUILD += xREADME.md
BUILD += docs
include Python.mk

#-------------------------------------------------------------------------------

.PHONY:		lscolors-samples
lscolors-samples:
		$(PYTHON) -m lscolors samples --force
clean::
		rm -rf lscolors-samples

#-------------------------------------------------------------------------------

.PHONY:		docs
docs:
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) docs --force

#-------------------------------------------------------------------------------

.PHONY:		xREADME.md
xREADME.md:
	{ \
		COLUMNS=97 $(PYTHON) -m lscolors --help | $(PYTHON) -m mandown \
			--name "$(PACKAGE)" \
			--title "$(PACKAGE_DESC)" \
			--no-footer; \
		for cmd in chart check configs report samples; do \
			echo "\n$(BAR2)\n"; \
			COLUMNS=97 $(PYTHON) -m lscolors $$cmd --help | $(PYTHON) -m mandown \
				--name "$(PACKAGE) $$cmd" \
				--title "$(PACKAGE) $$cmd" \
				--no-manpage-title \
				--no-name \
				--no-footer; \
		done; \
		echo "\n$(BAR2)\n"; \
		cmd=sort; \
		COLUMNS=97 $(PYTHON) -m lscolors $$cmd --help | $(PYTHON) -m mandown \
			--name "$(PACKAGE) $$cmd" \
			--title "$(PACKAGE) $$cmd" \
			--no-manpage-title \
			--no-name; \
       } >README.md

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
