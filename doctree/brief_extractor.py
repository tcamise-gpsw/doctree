from __future__ import annotations

from typing import Any
from pathlib import Path

from doctree import CommentType, File


class DocTree:
    def __init__(self, top_level: Path) -> None:
        self._top = top_level

    def __enter__(self) -> DocTree:
        ...

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

    @staticmethod
    def _discover_comment_type(file: Path) -> CommentType:
        ...

    @staticmethod
    def _extract_brief(file: Path) -> File:
        ...
