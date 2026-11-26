"""Detect direct reads of platform-specific environment variables."""

import ast


def find_platform_specific_env_vars(source: str) -> list[tuple[int, str]]:
    """Return direct reads of Windows-specific environment variables in *source*.

    Each finding is a one-based line number and a variable name, in source
    order. The rule matches literal ``os.environ[...]`` reads of ``APPDATA``
    and ``LOCALAPPDATA``. The source is parsed without executing it.
    """
    findings = []
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Subscript) or not isinstance(node.ctx, ast.Load):
            continue

        environ = node.value
        key = node.slice
        if (
            isinstance(environ, ast.Attribute)
            and environ.attr == "environ"
            and isinstance(environ.value, ast.Name)
            and environ.value.id == "os"
            and isinstance(key, ast.Constant)
            and isinstance(key.value, str)
            and key.value in ("APPDATA", "LOCALAPPDATA")
        ):
            findings.append((node.lineno, node.col_offset, key.value))

    findings.sort()
    return [(line_number, variable) for line_number, _, variable in findings]
