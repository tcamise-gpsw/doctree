from pathlib import Path

from git.repo.base import Repo


def get_all_files(top_level: Path) -> set[Path]:
    return set(top_level.rglob("*"))


def filter_git_ignored(files: set[Path]) -> set[Path]:
    try:
        with Repo(next(iter(files), None), search_parent_directories=True) as repo:
            ignored = set(Path(file) for file in repo.ignored(list(files)))
            return files.difference(ignored)
    # TODO what exception is returned if no git is found?
    except Exception as e:
        return files
