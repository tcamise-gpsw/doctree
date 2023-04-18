from pathlib import Path

from doctree.dir_parser import get_all_files, filter_git_ignored
from . import TEST_DIR, TEST_VECTOR_DIR


def test_get_all_files():
    assert len(get_all_files(Path(TEST_DIR)))


def test_filter_git_ignored():
    ignored_file = TEST_VECTOR_DIR / "ignored_file"
    files = get_all_files(Path(TEST_DIR))
    assert ignored_file in files
    filtered = filter_git_ignored(files)
    assert ignored_file not in filtered
