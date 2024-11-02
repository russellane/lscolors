# Python.mk - build/packaging tools for python/pdm projects
#
# Targets:				   [----per pyproject.toml----]
#  make [build]		pdm-install, tags, [black, pylint, pytest, etc], pdm-build
#  make clean		remove objs, caches, etc.
#  make clean-all	clean, dist, __pypackages__
#  make publish		copy wheel ~/packages
#  make bump-major	increment major part in libcurses/__version__.py
#  make bump-minor	increment minor part in libcurses/__version__.py
#  make bump-micro	increment micro part in libcurses/__version__.py
#  make install		pipx install, if console.scripts
#  make uninstall	pipx uninstall, if console.scripts
#  make reinstall	pipx uninstall && pipx install (not pipx reinstall)
#
# This file is common to multiple python/pdm projects, and is included by each of their
# Makefiles.  This file is maintained within one project; copies/clones of
# it exist in other projects.
#
# The purpose of this file is to separate common python build/packaging
# tasks from any customizations a project may require. Do not modify this
# file; `include` it in a top-level Makefile that defines required variable
# `PACKAGE`, and add customizations to that Makefile.
#
# Minimum Makefile (2 lines):
#	PACKAGE := mypackage
#	include Python.mk

#-------------------------------------------------------------------------------

ifeq ("$(PACKAGE)","")
	$(error PACKAGE is not defined)
endif

ifeq ("$(PACKAGE_NAME)","")
	PACKAGE_NAME := $(PACKAGE)
endif

#-------------------------------------------------------------------------------
# By default, "make [build]" runs known python tasks listed in `pyproject.toml`.

PYPROJECT_TOML := pyproject.toml
BUILD += tags $(shell $(SED) -n 's/^    "\(\(black\|isort\|flake8\|pydoctest\|pylint\|pytest\)\)[=<>~].*/\1/p' <$(PYPROJECT_TOML))

# "make bump-major/minor/micro" modifies this file:
VERSION_FILE := $(PACKAGE)/__version__.py

# "make publish" copies wheels to this directory:
PACKAGES := ~/packages

AWK := /bin/awk
GREP := /bin/grep
SED := /bin/sed

# Add other tasks to the default build list by adding to the `BUILD` variable in the top-level Makefile.
# For example, this file defines `README.md`, which uses `mandown` to create documentation.
#	PACKAGE := mypackage
#	BUILD += README.md
#	include Python.mk
#
# Add custom rules to the top-level Makefile as well, and add their targets to BUILD.
#	PACKAGE := mypackage
#	BUILD += task1
#	BUILD += task2
#	include Python.mk
#	task1:
#		echo running task1
#	task2:
#		echo running task2
#
# Note that Makefile adds to BUILD before including Python.mk

#-------------------------------------------------------------------------------
# This file implements these high-level targets:

# 1) make [build]	# tags, black, isort, flake8, pydoctest, pylint, pytest, pdm-build
# 2) make clean		# remove objs, caches, etc.
# 4) make clean-all	# clean + remove dist + remove env
# 5) make publish	# bump version, copy wheel ~/packages
# 6) make install	# pipx install if console.scripts
# 7) make uninstall	# pipx uninstall if console.scripts
# 8) make reinstall	# pipx uninstall && pipx install (not pipx reinstall)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# try this in .vimrc
# execute "set <M-m>=\em"
# execute "set <M-M>=\eM"
# nmap <M-m> :make
# nmap <M-M> :!xmake

# use :!make, not :make, for targets that use DEBUG_PAGER
DEBUG_PAGER	:= 2>&1 | more

BAR		= ---------------------------------------------------------------------- $(PACKAGE) $@
BAR2		:= --------------------------------------------------------------------------------
PYTHON		:= pdm run python
PYTHON_FILES	:= $(shell git ls-files '*.py')
PIPX		:= $(shell $(GREP) -q "^\[project.scripts\]" $(PYPROJECT_TOML) && echo pipx || echo 'echo no console_scripts to')

SRC_DIRS = $(PACKAGE)
ifneq ("$(wildcard tests)","")
	SRC_DIRS += tests
endif

.SUFFIXES:
.DEFAULT_GOAL = build

HELP = "Targets:				   [----per pyproject.toml----]\n"
.PHONY:	help
help:
	@echo $(HELP)

#-------------------------------------------------------------------------------
HELP += "make [build]\t\tpdm-install, $(TASKS), pdm-build\n"
comma = ", "
TASKS = $(subst $() $(),$(comma),$(BUILD))

.PHONY:		build .builder
build::		env bootstrap-deps .builder $(BUILD)
		pdm build

.builder:
		@echo $(BAR)
		@echo $(PACKAGE) building $(BUILD)

.PHONY:		env
env:		__pypackages__
__pypackages__:
		pdm install

.PHONY:		bootstrap-deps
bootstrap-deps:
	@echo $(BAR)
	{ \
		CMDS=$$($(GREP) '^# pdm add' $(PYPROJECT_TOML) | $(SED) 's/..//'); \
		if [ "$$CMDS" ]; then \
			EDITED=$$($(SED) '/^# pdm add/d' $(PYPROJECT_TOML)); \
			echo "$$EDITED" >$(PYPROJECT_TOML); \
			echo "$$CMDS" | bash -x; \
			echo "$(PYPROJECT_TOML) has been modified; please re-run $(MAKE) $(MFLAGS)"; \
			exit 1; \
		fi; \
	}

#-------------------------------------------------------------------------------
HELP += "make clean\t\tremove objs, caches, etc.\n"

.PHONY:		clean
clean::
		@echo $(BAR)
		rm -f .make.out
		find . -type f -name '*.py[co]' -delete && \
			find . -type d -name '__pycache__' -delete

#-------------------------------------------------------------------------------
HELP += "make clean-all\t\tclean, dist, __pypackages__\n"

.PHONY:		clean-all
clean-all::	clean
		rm -rf __pypackages__
		rm -rf dist

#-------------------------------------------------------------------------------
HELP += "make publish\t\tcopy wheel $(PACKAGES)\n"

.PHONY:		publish
publish:
		@echo $(BAR)
		/bin/mkdir -p $(PACKAGES)
		/bin/cp -p -v dist/*.whl $(PACKAGES)

#-------------------------------------------------------------------------------
HELP += "make bump-major\tincrement major part in $(VERSION_FILE)\n"
HELP += "make bump-minor\tincrement minor part in $(VERSION_FILE)\n"
HELP += "make bump-micro\tincrement micro part in $(VERSION_FILE)\n"

.PHONY:		bump-major .major-bumper
bump-major:	.major-bumper build
.major-bumper:
		@echo $(BAR)
		@echo Bumping version major level
		VERSION=`$(AWK) '/^__version__/ { split(substr($$3, 2), a, "."); \
			print a[1] + 1 ".0.0"}' <$(VERSION_FILE)`; \
		echo VERSION=$$VERSION; \
		echo '"""Version."""'"\n\n__version__ = \""$$VERSION'"' >$(VERSION_FILE)

.PHONY:		bump-minor .minor-bumper
bump-minor:	.minor-bumper build
.minor-bumper:
		@echo $(BAR)
		@echo Bumping version minor level
		VERSION=`$(AWK) '/^__version__/ { split(substr($$3, 2), a, "."); \
			print a[1] "." a[2] + 1 ".0"}' <$(VERSION_FILE)`; \
		echo VERSION=$$VERSION; \
		echo '"""Version."""'"\n\n__version__ = \""$$VERSION'"' >$(VERSION_FILE)

.PHONY:		bump-micro .micro-bumper
bump-micro:	.micro-bumper build
.micro-bumper:
		@echo $(BAR)
		@echo Bumping version micro level
		VERSION=`$(AWK) '/^__version__/ { split(substr($$3, 2), a, "."); \
			print a[1] "." a[2] "." a[3] + 1}' <$(VERSION_FILE)`; \
		echo VERSION=$$VERSION; \
		echo '"""Version."""'"\n\n__version__ = \""$$VERSION'"' >$(VERSION_FILE)

#-------------------------------------------------------------------------------
HELP += "make install\t\tpipx install, if console.scripts\n"

.PHONY:		install
install:
		@echo $(BAR)
		$(PIPX) install $(PACKAGE_NAME)

#-------------------------------------------------------------------------------
HELP += "make uninstall\t\tpipx uninstall, if console.scripts\n"

.PHONY:		uninstall
uninstall:
		@echo $(BAR)
		-$(PIPX) uninstall $(PACKAGE_NAME)

#-------------------------------------------------------------------------------
HELP += "make reinstall\t\tpipx uninstall && pipx install (not pipx reinstall)"

.PHONY:		reinstall
reinstall:	uninstall install
		@echo $(BAR)

#-------------------------------------------------------------------------------
# BUILD targets
#-------------------------------------------------------------------------------

.PHONY:		tags
tags:
		ctags -R $(SRC_DIRS)

clean::
		rm -f tags

#-------------------------------------------------------------------------------

.PHONY:		black flake8 isort pylint
black flake8 isort pylint:
		@echo $(BAR)
		$(PYTHON) -m $@ $(SRC_DIRS)

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
		find . -name .pytest_cache | xargs -rt rm -rf

#-------------------------------------------------------------------------------

SRC_APP_NO_MAIN := $(filter-out $(PACKAGE)/__main__.py, $(PYTHON_FILES))

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

.PHONY:		pydoc
pydoc:
		for i in $(PYTHON_FILES); do LESS=c$$LESS $(PYTHON) -m pydoc $$i; done

#-------------------------------------------------------------------------------

.PHONY:		README.md
README.md:
	{ \
		export COLUMNS=97; \
		WIDTH=89; \
		pdm run $(PACKAGE) --help | pdm run mandown \
			$(MANDOWN_OPTS) --width $$WIDTH --use-config; \
	} >$@

#-------------------------------------------------------------------------------
# vim: set ts=8 sw=8 noet:
