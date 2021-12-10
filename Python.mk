# This file is common to numerous projects, and is included by each of their
# Makefiles.  This file is maintained within one project; copies/clones of
# it exist in other projects.

#-------------------------------------------------------------------------------
# This file implements these high-level targets:

# 1) make [build]	# black, isort, flake8, pydocstyle, pydoctest, pylint, pytest && dist
# 2) make clean
# 3) make dist		# poetry build
# 4) make distclean
# 5) make publish	# poetry version patch && copy wheels ~/packages
# 6) make install	# pipx install if console.scripts
# 7) make uninstall	# pipx uninstall if console.scripts
# 8) make reinstall	# pipx uninstall && pipx install (not pipx reinstall)
# 9) make full		# really-build publish reinstall

# Undocumented:
# default
# doctest-debug
# pydocstyle
# pytest-info
# build-venv
# pytest-pdb
# clean-poetry.lock
# really-rebuild
# clean-venv
# pydoc
# pytest-debug
# rebuild

#-------------------------------------------------------------------------------
# A project's Makefile defines the list of components the project is to
# build. Copy and uncomment the desired lines into the project's Makefile.
# Uncommenting them here will apply to all projects. These components
# are available:

BUILD := tags $(shell egrep '^(black|isort|flake8|pydocstyle|pydoctest|pylint|pytest) = ' <pyproject.toml | cut -d' ' -f1) $(BUILD)

#-------------------------------------------------------------------------------
# try this in .vimrc
# execute "set <M-m>=\em"
# execute "set <M-M>=\eM"
# nmap <M-m> :make
# nmap <M-M> :!xmake

# use :!make, not :make, for targets that use DEBUG_PAGER
DEBUG_PAGER	:= 2>&1 | more

.SUFFIXES:

BAR		= ---------------------------------------------------------------------- $(PACKAGE) $@
BAR2		:= --------------------------------------------------------------------------------
PYTHON		:= poetry run python
SRC_ALL		:= $(shell git ls-files '*.py')
SRC_APP		:= $(filter-out setup.py, $(SRC_ALL))
PACKAGE_NAME	:= $(shell python -c 'import tomlkit; t = tomlkit.loads(open("pyproject.toml").read()); print(t["tool"]["poetry"]["name"])')
PACKAGE_DESC	:= $(shell python -c 'import tomlkit; t = tomlkit.loads(open("pyproject.toml").read()); print(t["tool"]["poetry"]["description"])')
PIPX		:= $(shell grep -q "^\[tool.poetry.scripts\]" pyproject.toml && echo pipx || echo 'echo no console_scripts to')

#-------------------------------------------------------------------------------
# 1) make [build]

.PHONY:		build
default:	build
build::		builder $(BUILD) dist

.PHONY:		builder
builder:
		@echo $(BAR)
		@echo $(PACKAGE) building $(BUILD)

.PHONY:		rebuild
rebuild:	rebuilder build-venv build

.PHONY:		rebuilder
rebuilder:
		@echo $(PACKAGE) re-building $(BUILD)

.PHONY:		really-rebuild
really-rebuild:	really-rebuilder clean-venv clean-poetry.lock bootstrap-deps rebuild

.PHONY:		really-rebuilder
really-rebuilder:
		@echo $(PACKAGE) really-re-building $(BUILD)

.PHONY:		build-venv
build-venv:
		@echo $(BAR)
		poetry install

.PHONY:		clean-venv
clean-venv:
		@echo $(BAR)
		venv=$$(poetry env list | awk "{print \$$1}"); [ "$$venv" ] \
			&& poetry env remove $$venv \
			|| echo no venv to clean

.PHONY:		clean-poetry.lock
clean-poetry.lock:
		@echo $(BAR)
		rm -f poetry.lock

.PHONY:		bootstrap-deps
bootstrap-deps:
		@echo $(BAR)
		{ \
			CMDS=$$(/bin/grep '^# poetry add' pyproject.toml | sed 's/..//'); \
			if [ "$$CMDS" ]; then \
				EDITED=$$(/bin/sed '/^# poetry add/d' pyproject.toml); \
				echo "$$EDITED" >pyproject.toml; \
				echo "$$CMDS" | bash -x; \
			fi; \
		}

#-------------------------------------------------------------------------------
# 2) make clean

.PHONY:		clean
clean::
		@echo $(BAR)
		rm -f .make.out
		find . -type f -name '*.py[co]' -delete && \
			find . -type d -name '__pycache__' -delete

#-------------------------------------------------------------------------------
# 3) make dist

.PHONY:		dist
dist:		clean-dist
		@echo $(BAR)
		poetry build

.PHONY:		clean-dist
clean::		clean-dist
clean-dist:
		@echo $(BAR)
		rm -rf dist

#-------------------------------------------------------------------------------
# 4) make distclean

.PHONY:		distclean
distclean::	clean clean-venv

#-------------------------------------------------------------------------------
# 5) make publish

.PHONY:		publish
publish:	publisher build
		@echo $(BAR)
		/bin/cp -p -v dist/*.whl ~/packages

.PHONY:		publisher
publisher:
		@echo $(BAR)
		poetry version patch
		echo '"""Version."""'"\n\n__version__ = \""`poetry version --short`'"' >$(PACKAGE)/__version__.py

#-------------------------------------------------------------------------------
# 6) make install

.PHONY:		install
install:
		@echo $(BAR)
		$(PIPX) install $(PACKAGE_NAME)

#-------------------------------------------------------------------------------
# 7) make uninstall

.PHONY:		uninstall
uninstall:
		@echo $(BAR)
		-$(PIPX) uninstall $(PACKAGE_NAME)

#-------------------------------------------------------------------------------
# 8) make reinstall

.PHONY:		reinstall
reinstall:	uninstall install
		@echo $(BAR)

#-------------------------------------------------------------------------------
# 9) make full

.PHONY:		full
full:		really-rebuild publish reinstall

#-------------------------------------------------------------------------------
# BUILD targets
#-------------------------------------------------------------------------------

.PHONY:		tags
tags:
		@echo $(BAR)
		ctags -R --languages=python $(SRC_APP)

clean::
		@echo $(BAR)
		rm -f tags

#-------------------------------------------------------------------------------

.PHONY:		flake8
flake8:
		@echo $(BAR)
		$(PYTHON) -m flake8 $(SRC_ALL)

#-------------------------------------------------------------------------------

.PHONY:		pylint
pylint:
		@echo $(BAR)
		$(PYTHON) -m pylint $(SRC_ALL)

#-------------------------------------------------------------------------------

PYTEST :=	$(PYTHON) -m pytest --cache-clear --exitfirst --showlocals --verbose

.PHONY:		pytest
pytest:
		@echo $(BAR)
		$(PYTEST)

.PHONY:		pytest-info
pytest-info:
		{ set -x; $(PYTEST) --log-cli-level INFO --capture=no; } $(DEBUG_PAGER)

.PHONY:		pytest-debug
pytest-debug:
		{ set -x; $(PYTEST) --log-cli-level DEBUG --capture=no; } $(DEBUG_PAGER)

.PHONY:		pytest-pdb
pytest-pdb:
		$(PYTEST) --capture=no --pdb

clean::
		@echo $(BAR)
		find . -name .pytest_cache | xargs -rt rm -rf

#-------------------------------------------------------------------------------

SRC_APP_NO_MAIN := $(filter-out $(PACKAGE)/__main__.py, $(SRC_APP))

.PHONY:		pydoctest
DOCTEST :=	$(PYTHON) -m doctest
pydoctest:
		@echo $(BAR)
		$(DOCTEST) $(SRC_APP_NO_MAIN)

.PHONY:		pydoctest-debug
pydoctest-debug:
		for i in $(SRC_APP_NO_MAIN); do \
			echo $(BAR); \
			echo $$i; \
			echo $(BAR); \
			$(DOCTEST) -v $$i; \
		done $(DEBUG_PAGER)

#-------------------------------------------------------------------------------

.PHONY:		pydocstyle
pydocstyle:
		@echo $(BAR)
		outfile=`mktemp`; \
		$(PYTHON) -m pydocstyle $(PACKAGE) | \
			while read x; do read y; echo $$(echo $$x | awk "{print \$$1}"):0 $$y; done | \
			sort -k2 -k1 | tee $$outfile; \
		[ -s $$outfile ]; ret=$$?; rm -f $$outfile; [ $$ret -ne 0 ]

#-------------------------------------------------------------------------------

.PHONY:		pydoc
pydoc:
		for i in $(SRC_APP); do LESS=c$$LESS $(PYTHON) -m pydoc $$i; done

#-------------------------------------------------------------------------------

.PHONY:		black
black:
		@echo $(BAR)
		$(PYTHON) -m black $(SRC_ALL)

#-------------------------------------------------------------------------------

.PHONY:		isort
isort:
		@echo $(BAR)
		$(PYTHON) -m isort $(SRC_ALL)

#-------------------------------------------------------------------------------

.PHONY:		README.md
README.md:
		COLUMNS=97 $(PYTHON) -m $(PACKAGE) --help | $(PYTHON) -m mandown \
			--name "$(PACKAGE)" \
			--title "$(PACKAGE_DESC)" $(MANDOWN_OPTS) >$@

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
