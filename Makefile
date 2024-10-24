PROJECT	:=	lscolors

build:		__pypackages__ ctags lint test coverage README.md
		pdm build

.PHONY:		README.md
README.md:
		python -m $(PROJECT) --md-help >$@

publish:
		cd dist; echo *.whl | cpio -pdmuv `pip config get global.find-links`

install:
		-pipx uninstall $(PROJECT)
		pipx install $(PROJECT)

bump_micro:	_bump_micro clean build
_bump_micro:
		pdm bump micro

__pypackages__:
		pdm install

.PHONY:		ctags
ctags:
		ctags -R $(PROJECT) tests __pypackages__ 

lint:		black isort flake8 mypy

black:
		python -m black -q $(PROJECT) tests

isort:
		python -m isort $(PROJECT) tests

flake8:
		python -m flake8 $(PROJECT) tests

mypy::
		python -m mypy $(PROJECT) tests

test:
		python -m pytest --exitfirst --showlocals --verbose tests

test_debug:
		python -m pytest --exitfirst --showlocals --verbose --capture=no tests

coverage:
		python -m pytest --cov=$(PROJECT) tests

cov_html:
		python -m pytest --cov=$(PROJECT) --cov-report=html tests

clean:
		rm -rf .coverage .mypy_cache .pdm-build .pytest_cache __pypackages__ dist htmlcov tags 
		find . -type f -name '*.py[co]' -delete
		find . -type d -name __pycache__ -delete
