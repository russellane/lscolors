# This file is common to numerous projects, and is included by each of their
# Makefiles.  This file is maintained within one project; copies/clones of
# it exist in other projects.

ifeq ("$(PACKAGE)","")
    $(error PACKAGE is not defined)
endif

#-------------------------------------------------------------------------------
# High-level targets:
#
#	[build]		# poetry install + black/isort/flake8/pydoctest/pylint/pytest + $(BUILD) + poetry build
#	clean		# remove *.py[co], __pycache__, dist
#	distclean	# remove *.py[co], __pycache__, dist + poetry env remove
#	publish		# poetry version patch + build + copy wheels to ~/packages
#	install		# pipx install if console.scripts
#	uninstall	# pipx uninstall if console.scripts
#	reinstall	# pipx uninstall + pipx install (not pipx reinstall)

# Undocumented:
# doctest-debug
# pytest-info
# pytest-pdb
# clean-poetry.lock
# really-rebuild
# build-venv
# clean-venv
# pydoc
# pytest-debug
# rebuild

#-------------------------------------------------------------------------------
# try this in .vimrc
# execute "set <M-m>=\em"
# execute "set <M-M>=\eM"
# nmap <M-m> :make
# nmap <M-M> :!xmake

# use :!make, not :make, for targets that use DEBUG_PAGER
DEBUG_PAGER	:= 2>&1 | more

__bar__		= ---------------------------------------------------------------------- $(PACKAGE) $@
PYTHON		:= poetry run python
SRC_FILES	:= $(shell git ls-files '*.py')
PACKAGE_NAME	:= $(shell python -c 'import tomlkit; t = tomlkit.loads(open("pyproject.toml").read()); print(t["tool"]["poetry"]["name"])')
PIPX		:= $(shell grep -q "^\[tool.poetry.scripts\]" pyproject.toml && echo pipx || echo 'echo no console_scripts to')
BUILD		:= tags $(shell egrep '^(black|isort|flake8|pydoctest|pylint|pytest) = ' <pyproject.toml | cut -d' ' -f1) $(BUILD)

SRC_DIRS = $(PACKAGE)
ifneq ("$(wildcard tests)","")
    SRC_DIRS += tests
endif

.SUFFIXES:
default:	build

#-------------------------------------------------------------------------------
# 1) make [build]

.PHONY:		build
build::		builder build-venv $(BUILD)
		@echo $(__bar__)
		rm -rf dist
		poetry build

.PHONY:		builder
builder:
		@echo $(__bar__)
		@echo $(PACKAGE) building $(BUILD)

.PHONY:		rebuild
rebuild:	rebuilder build-venv build

.PHONY:		rebuilder
rebuilder:
		@echo $(PACKAGE) re-building $(BUILD)

.PHONY:		really-rebuild
really-rebuild:	really-rebuilder clean-venv clean-poetry.lock rebuild

.PHONY:		really-rebuilder
really-rebuilder:
		@echo $(PACKAGE) really-re-building $(BUILD)

.PHONY:		build-venv
build-venv::
		@echo $(__bar__)
		poetry install

.PHONY:		clean-venv
clean-venv::
		@echo $(__bar__)
		venv=$$(poetry env list | awk "{print \$$1}"); [ "$$venv" ] \
			&& poetry env remove $$venv \
			|| echo no venv to clean

.PHONY:		clean-poetry.lock
clean-poetry.lock:
		@echo $(__bar__)
		rm -f poetry.lock

#-------------------------------------------------------------------------------
# 2) make clean

.PHONY:		clean
clean::
		@echo $(__bar__)
		rm -f .make.out
		find . -type f -name '*.py[co]' -delete
		find . -type d -name '__pycache__' -delete
		rm -rf dist

#-------------------------------------------------------------------------------
# 4) make distclean

.PHONY:		distclean
distclean::	clean clean-venv

#-------------------------------------------------------------------------------
# 5) make publish

.PHONY:		publish
publish:	publisher build
		@echo $(__bar__)
		/bin/cp -p -v dist/*.whl ~/packages

.PHONY:		publisher
publisher:
		@echo $(__bar__)
		poetry version patch
		echo '"""Version."""'"\n\n__version__ = \""`poetry version --short`'"' >$(PACKAGE)/__version__.py

#-------------------------------------------------------------------------------
# 6) make install

.PHONY:		install
install:
		@echo $(__bar__)
		$(PIPX) install $(PACKAGE_NAME)

#-------------------------------------------------------------------------------
# 7) make uninstall

.PHONY:		uninstall
uninstall:
		@echo $(__bar__)
		-$(PIPX) uninstall $(PACKAGE_NAME)

#-------------------------------------------------------------------------------
# 8) make reinstall

.PHONY:		reinstall
reinstall:	uninstall install
		@echo $(__bar__)

#-------------------------------------------------------------------------------
# BUILD targets
#-------------------------------------------------------------------------------

.PHONY:		tags
tags:
		@echo $(__bar__)
		ctags -R $(SRC_DIRS)

clean::
		@echo $(__bar__)
		rm -f tags

#-------------------------------------------------------------------------------

.PHONY:		black flake8 isort pylint
black flake8 isort pylint:
		@echo $(__bar__)
		$(PYTHON) -m $@ $(SRC_DIRS)

#-------------------------------------------------------------------------------

PYTEST :=	$(PYTHON) -m pytest --cache-clear --exitfirst --showlocals --verbose

.PHONY:		pytest
pytest:
		@echo $(__bar__)
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
		@echo $(__bar__)
		find . -name .pytest_cache | xargs -rt rm -rf

#-------------------------------------------------------------------------------

SRC_APP_NO_MAIN := $(filter-out $(PACKAGE)/__main__.py, $(SRC_FILES))

.PHONY:		pydoctest
DOCTEST :=	$(PYTHON) -m doctest
pydoctest:
		@echo $(__bar__)
		$(DOCTEST) $(SRC_APP_NO_MAIN)

.PHONY:		pydoctest-debug
pydoctest-debug:
		for i in $(SRC_APP_NO_MAIN); do \
			echo $(__bar__); \
			echo $$i; \
			echo $(__bar__); \
			$(DOCTEST) -v $$i; \
		done $(DEBUG_PAGER)

#-------------------------------------------------------------------------------

.PHONY:		pydoc
pydoc:
		for i in $(SRC_FILES); do LESS=c$$LESS $(PYTHON) -m pydoc $$i; done

#-------------------------------------------------------------------------------

.PHONY:		README.md
README.md:
	{ \
		export COLUMNS=97; \
		WIDTH=89; \
		$(PYTHON) -m $(PACKAGE) --help | $(PYTHON) -m mandown \
			$(MANDOWN_OPTS) --width $$WIDTH --use-config; \
	} >$@

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
