import pytest

from lscolors.cli import main


@pytest.mark.parametrize(
    ("command"),
    [
        ("chart"),
        ("check"),
        ("configs"),
        ("docs"),
        ("paint"),
        ("report"),
        ("samples"),
        ("sort"),
    ],
)
def test_help(command: str) -> None:
    with pytest.raises(SystemExit) as err:
        main([command, "--help"])
    assert err.value.code == 0
