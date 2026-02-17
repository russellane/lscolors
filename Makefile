include Python.mk
PROJECT = lscolors
COV_FAIL_UNDER = 32
lint :: mypy
doc :: README.md
