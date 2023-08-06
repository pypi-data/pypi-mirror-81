import logging
import sys
from pathlib import Path
import os
import tempfile
import shutil
import pytest


@pytest.fixture
def test_dir():
    module_dir = Path(__file__).resolve().parent
    test_dir = module_dir / "test_data"
    return test_dir.resolve()


@pytest.fixture
def example_dir():
    root_dir = Path(__file__).resolve().parent.parent
    example_dir = root_dir / "examples"
    return example_dir.resolve()


@pytest.fixture
def log_to_stdout():
    # Set Logging
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)


@pytest.fixture
def clean_dir():
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)
