"""The entrypoint for the doctree tool"""

from pathlib import Path

from doctree import DocTree


def entrypoint() -> None:
    main()


def main() -> None:
    with DocTree(Path(".")) as tree:
        print(tree.as_markdown)


if __name__ == "__main__":
    main()
