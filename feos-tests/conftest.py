import shutil, subprocess, sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parent.parent
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sample"

@pytest.fixture
def repo(tmp_path):
    """Copy of the FEOS kit + sample project, so scripts (which resolve ROOT from their own path) run isolated."""
    dst = tmp_path / "repo"
    shutil.copytree(REPO, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", ".feos", "evidence", "feos-tests"))
    shutil.copytree(FIXTURE, dst, dirs_exist_ok=True)
    return dst

def run(repo, *args, stdin=None, env=None):
    return subprocess.run([sys.executable, *args], cwd=repo, capture_output=True, text=True, input=stdin, env=env)
