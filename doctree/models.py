import enum
from pathlib import Path
from typing import Optional

from dataclasses import dataclass

import pyparsing


class CommentType(enum.Enum):
    SLASH_STAR = pyparsing.c_style_comment  # ``/* ... */``
    HTML_STYLE = pyparsing.html_comment  # ``<!-- ... -->``
    DOUBLE_SLASH = pyparsing.dbl_slash_comment  # ``// ... (to end of line)``
    HASH = pyparsing.python_style_comment  # ``# ... (to end of line)``


class ErrorType(enum.Enum):
    SUCCESS = enum.auto()
    FAILURE = enum.auto()


@dataclass
class Error:
    type: ErrorType
    detail: Optional[str] = None


@dataclass
class File:
    name: str
    path: Path
    brief: str
    comment_type: CommentType
    status: Error
