PACKAGE := lscolors
BUILD += PKG-README
BUILD += README
BUILD += README.md
include Python.mk

#-------------------------------------------------------------------------------

.PHONY:		lscolors-samples
lscolors-samples:
		$(PYTHON) -m lscolors samples --force
clean::
		rm -rf lscolors-samples

#-------------------------------------------------------------------------------

.PHONY:		PKG-README
PKG-README:
		$(PYTHON) -m lscolors --help >$@

#-------------------------------------------------------------------------------

.PHONY:		README
README:
	{ \
		$(PYTHON) -m lscolors --help; \
		for cmd in chart check configs report samples sort; do \
			echo "\n$(BAR2)\n"; \
			$(PYTHON) -m lscolors $$cmd --help; \
		done; \
	} >$@

#-------------------------------------------------------------------------------

.PHONY:		README.md
README.md:
	{ \
		$(PYTHON) -m lscolors --help | $(PYTHON) -m mandown \
			--name "$(PACKAGE)" \
			--title "$(PACKAGE_DESC)" \
			--no-footer; \
		for cmd in chart check configs report samples; do \
			echo "\n$(BAR2)\n"; \
			$(PYTHON) -m lscolors $$cmd --help | $(PYTHON) -m mandown \
				--name "$(PACKAGE) $$cmd" \
				--title "$(PACKAGE) $$cmd" \
				--no-manpage-title \
				--no-name \
				--no-footer; \
		done; \
		echo "\n$(BAR2)\n"; \
		cmd=sort; \
		$(PYTHON) -m lscolors $$cmd --help | $(PYTHON) -m mandown \
			--name "$(PACKAGE) $$cmd" \
			--title "$(PACKAGE) $$cmd" \
			--no-manpage-title \
			--no-name; \
       } >$@

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
