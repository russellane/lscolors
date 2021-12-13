"""lscolors mkdir."""

import pathlib
import shutil


def mkdir(path, force):
    """Create directory."""

    path = pathlib.Path(path)
    if path.exists():
        if not force:
            raise RuntimeError(f"Directory `{path}` already exists, try `--force`.")
        shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)
