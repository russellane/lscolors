import pytest

from lscolors.cli import main


def test_version():
    with pytest.raises(SystemExit) as err:
        main(["--version"])
    assert err.value.code == 0


def test_help():
    with pytest.raises(SystemExit) as err:
        main(["--help"])
    assert err.value.code == 0


def test_usage_option():
    with pytest.raises(SystemExit) as err:
        main(["--bogus-option"])
    assert err.value.code == 2


def test_usage_argument():
    with pytest.raises(SystemExit) as err:
        main(["bogus-argument"])
    assert err.value.code == 2


def test_print_config():
    with pytest.raises(SystemExit) as err:
        main(["--print-config"])
    assert err.value.code == 0
