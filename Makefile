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
			--title "$(PACKAGE_DESC)" $(MANDOWN_OPTS) \
			--no-footer; \
		for cmd in chart check configs report samples; do \
			echo "\n$(BAR2)\n"; \
			$(PYTHON) -m lscolors $$cmd --help | $(PYTHON) -m mandown \
				--no-manpage-title --no-name-section --no-footer; \
		done; \
		echo "\n$(BAR2)\n"; \
		$(PYTHON) -m lscolors sort --help | $(PYTHON) -m mandown \
			--no-manpage-title \
			--no-name-section; \
       } >$@

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
