import enum
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


class ErrorType(enum.Enum):
    SUCCESS = enum.auto()
    FAILURE = enum.auto()


@dataclass
class Status:
    type: ErrorType
    detail: Optional[str] = None


@dataclass
class File:
    name: str
    path: Path
    brief: str
    status: Error
