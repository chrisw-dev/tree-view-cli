import tempfile
from pathlib import Path

from src.tree_view_cli.tree_view_cli import DirectoryTreeGenerator


def test_basic_structure(temp_directory, capsys):
    tree_gen = DirectoryTreeGenerator(temp_directory)
    tree_gen.generate_tree()
    captured = capsys.readouterr()
    assert 'dir1' in captured.out
    assert 'subdir1' in captured.out
    assert 'subdir2' in captured.out
    assert 'file1.txt' in captured.out
    assert 'file2.txt' in captured.out
    assert 'file3.txt' in captured.out


def test_max_depth(temp_directory, capsys):
    tree_gen = DirectoryTreeGenerator(temp_directory, max_depth=1)
    tree_gen.generate_tree()
    captured = capsys.readouterr()
    assert 'dir1' in captured.out
    assert 'subdir1' not in captured.out
    assert 'file2.txt' not in captured.out


def test_gitignore_file(temp_directory, capsys):
    with open(temp_directory / '.gitignore', 'w', encoding='utf-8') as f:
        f.write('**/file1.txt\n')
    tree_gen = DirectoryTreeGenerator(temp_directory)
    tree_gen.generate_tree()
    captured = capsys.readouterr()
    assert 'file1.txt' not in captured.out
    assert 'file2.txt' in captured.out


def test_gitignore_directory(temp_directory, capsys):
    with open(temp_directory / '.gitignore', 'w', encoding='utf-8') as f:
        f.write('dir1/\n')
    tree_gen = DirectoryTreeGenerator(temp_directory)
    tree_gen.generate_tree()
    captured = capsys.readouterr()
    assert 'dir1' not in captured.out


def test_gitignore_subdirectory(temp_directory, capsys):
    with open(temp_directory / '.gitignore', 'w', encoding='utf-8') as f:
        f.write('**/subdir1\n')
    tree_gen = DirectoryTreeGenerator(temp_directory)
    tree_gen.generate_tree()
    captured = capsys.readouterr()
    assert 'subdir1' not in captured.out
    assert 'subdir2' in captured.out


def test_empty_directory(capsys):
    with tempfile.TemporaryDirectory() as empty_temp_directory:
        empty_temp = Path(empty_temp_directory)
        tree_gen = DirectoryTreeGenerator(empty_temp)
        tree_gen.generate_tree()
        captured = capsys.readouterr()
        assert captured.out.strip() == empty_temp.name + '/'


def test_git_directory_excluded(temp_directory, capsys):
    (temp_directory / '.git').mkdir()
    tree_gen = DirectoryTreeGenerator(temp_directory)
    tree_gen.generate_tree()
    captured = capsys.readouterr()
    assert 'dir1' in captured.out
    assert '.git' not in captured.out
