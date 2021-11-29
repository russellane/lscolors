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
			for cmd in check configs report samples sort; do \
				echo "\n$(BAR)\n"; \
				$(PYTHON) -m lscolors $$cmd --help; \
			done; \
		} >$@

#-------------------------------------------------------------------------------

.PHONY:		README.md
README.md:
		{ for cmd in \
			'lscolors' \
			'lscolors check' \
			'lscolors configs' \
			'lscolors report' \
			'lscolors samples' \
			'lscolors sort'; \
		    do \
			$(PYTHON) -m $$cmd --help | \
				$(PYTHON) -m mandown --no-manpage-title --no-name-section \
					--no-colophon --name "$$cmd" --title "$$cmd"; \
		    done; \
		    $(PYTHON) -m mandown --footer; \
	       } >$@

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
