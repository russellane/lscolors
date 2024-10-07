"""lscolors mkdir."""

import pathlib
import shutil


def mkdir(path: str, force: bool) -> None:
    """Create directory."""

    _path = pathlib.Path(path)
    if _path.exists():
        if not force:
            raise RuntimeError(f"Directory `{path}` already exists, try `--force`.")
        shutil.rmtree(_path, ignore_errors=True)
    _path.mkdir(parents=True)
