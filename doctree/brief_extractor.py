from __future__ import annotations
import logging
from pathlib import Path
from typing import Any, Optional

from pyparsing import (
    Suppress,
    rest_of_line,
    cpp_style_comment,
    html_comment,
    dbl_slash_comment,
    python_style_comment,
)

from doctree import File, Status, ErrorType
from doctree.dir_parser import get_all_files, filter_git_ignored

logger = logging.getLogger(__name__)


class DocTree:
    _comment_types = [
        cpp_style_comment,
        html_comment,
        dbl_slash_comment,
        python_style_comment,
    ]

    def __init__(self, top_level: Path, search_len: int = 20) -> None:
        self._top = top_level
        self._search_len = search_len
        self._tree: dict[str, Any] = {}

    def __enter__(self) -> DocTree:
        for file in filter_git_ignored(get_all_files(self._top)):
            brief = self._extract_brief(file)
            file = File(file.name, file, brief, Status(ErrorType.SUCCESS))


    def __exit__(self, exc_type, exc_value, exc_tb):
        ...

    @property
    def as_markdown(self) -> str:
        ...

    @property
    def as_json(self) -> dict[str, Any]:
        ...

    @property
    def errors(self) -> list[File]:
        ...

    ####################################################################################
    # End Public API
    ####################################################################################

    def _extract_brief(self, file: Path) -> str:
        # Extract lines that we will search
        searchable = ""
        with open(file) as fp:
            for _ in range(self._search_len):
                searchable += fp.readline()

        # Find all comment types and filter based on any that include the @brief token.
        # There should only be one. TODO how to handle multiple
        brief: Optional[str] = None
        for comment_type in self._comment_types:
            # Find all comments of this type
            for result in comment_type("doc").search_string(searchable):
                # See if this comment has our token
                if "@brief" in result.doc:
                    brief = result.doc
                    break
            if brief:
                break
        # TODO handle missing brief
        assert brief
        logger.debug(f"found brief: {brief}")

        # Get brief from comment
        comment = (Suppress("@brief") + rest_of_line("comment")).search_string(brief)
        return comment[0].comment.strip().strip("-->").strip()  # type: ignore
