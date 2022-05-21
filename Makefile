PROJECT	:=	lscolors

build:		__pypackages__ ctags black isort flake8 pytest README.md
		pdm build

.PHONY:		README.md
README.md:
		python -m $(PROJECT) --long-help >$@

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

ctags:
		ctags -R $(PROJECT) tests __pypackages__ 

black:
		python -m black -q $(PROJECT) tests

isort:
		python -m isort $(PROJECT) tests

flake8:
		python -m flake8 $(PROJECT) tests

pytest:
		python -m pytest --exitfirst --showlocals --verbose tests

clean:
		rm -rf __pypackages__ .pytest_cache dist tags
		find . -type f -name '*.py[co]' -delete
		find . -type d -name __pycache__ -delete
