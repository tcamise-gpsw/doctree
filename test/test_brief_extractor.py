from pathlib import Path

import pytest

from doctree import DocTree
from . import TEST_VECTOR_DIR

test_files = [path for path in TEST_VECTOR_DIR.rglob("*") if path.is_file() and "ignored" not in path.name]


@pytest.fixture
def doc_tree():
    yield DocTree(top_level=TEST_VECTOR_DIR, search_len=20)


@pytest.mark.parametrize("file", test_files)
def test_extract_briefs(file, doc_tree: DocTree):
    brief = doc_tree._extract_brief(file)
    assert brief == "TestBrief"
