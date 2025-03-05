import tempfile
from pathlib import Path

import pytest


def create_file_structure(
    root,
):
    (root / 'dir1' / 'subdir1').mkdir(parents=True)
    (root / 'dir1' / 'subdir2').mkdir(parents=True)
    (root / 'dir1' / 'file1.txt').touch()
    (root / 'dir1' / 'subdir1' / 'file2.txt').touch()
    (root / 'dir1' / 'subdir2' / 'file3.txt').touch()


@pytest.fixture
def temp_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        root = Path(tmpdirname)
        create_file_structure(root=root)
        yield Path(tmpdirname)
