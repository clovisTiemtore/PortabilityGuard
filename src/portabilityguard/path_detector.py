"""Detect hard-coded absolute paths in Python source code."""

import ast
from pathlib import PurePosixPath, PureWindowsPath


def is_absolute_path(path: str) -> bool:
    """Return whether *path* is absolute on POSIX or Windows."""
    return PurePosixPath(path).is_absolute() or PureWindowsPath(path).is_absolute()


def find_absolute_paths(source: str) -> list[tuple[int, str]]:
    """Return absolute path literals found in Python *source*.

    Each finding is represented by its one-based source line number and the
    literal path. The source is parsed, never executed.
    """
    tree = ast.parse(source)
    findings = [
        (node.lineno, node.col_offset, node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and is_absolute_path(node.value)
    ]
    findings.sort(key=lambda finding: (finding[0], finding[1]))
    return [(line_number, path) for line_number, _, path in findings]
