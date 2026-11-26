"""Detect text-mode ``open()`` calls without an explicit encoding."""

import ast

MISSING_ENCODING_MESSAGE = (
    "open() uses text mode without an explicit encoding; results may vary across "
    "platforms."
)


def _is_valid_file_mode(mode: str) -> bool:
    """Return whether *mode* is a statically valid mode for ``open()``."""
    allowed_characters = set("rwaxbt+")
    access_modes = "rwax"

    return (
        bool(mode)
        and set(mode) <= allowed_characters
        and sum(mode.count(character) for character in access_modes) == 1
        and all(mode.count(character) <= 1 for character in allowed_characters)
        and not ("b" in mode and "t" in mode)
    )


def _is_direct_open_call(node: ast.Call) -> bool:
    """Return whether *node* calls the direct name ``open``."""
    return isinstance(node.func, ast.Name) and node.func.id == "open"


def _has_file_argument(node: ast.Call) -> bool:
    """Return whether *node* supplies exactly one file argument."""
    file_keywords = [keyword for keyword in node.keywords if keyword.arg == "file"]
    return (bool(node.args) and not file_keywords) or (
        not node.args and len(file_keywords) == 1
    )


def _has_explicit_encoding(node: ast.Call) -> bool:
    """Return whether *node* supplies an encoding other than literal ``None``."""
    encoding_arguments = []
    if len(node.args) >= 4:
        encoding_arguments.append(node.args[3])
    encoding_arguments.extend(
        keyword.value for keyword in node.keywords if keyword.arg == "encoding"
    )

    return any(
        not isinstance(argument, ast.Constant) or argument.value is not None
        for argument in encoding_arguments
    )


def _text_mode(node: ast.Call) -> bool | None:
    """Return the static text-mode status, or ``None`` if it is indeterminate."""
    mode_keywords = [keyword for keyword in node.keywords if keyword.arg == "mode"]
    if len(mode_keywords) > 1 or (len(node.args) >= 2 and mode_keywords):
        return None

    if len(node.args) >= 2:
        mode_node = node.args[1]
    elif mode_keywords:
        mode_node = mode_keywords[0].value
    else:
        return True

    if not isinstance(mode_node, ast.Constant) or not isinstance(mode_node.value, str):
        return None

    mode = mode_node.value
    if not _is_valid_file_mode(mode):
        return None
    return "b" not in mode


def find_missing_encodings(source: str) -> list[tuple[int, str]]:
    """Return text-mode ``open()`` calls lacking an explicit encoding.

    Each finding contains the call's one-based source line number and an
    explanatory message. The Python source is parsed with :mod:`ast` and is
    never executed. Calls with dynamic modes or unpacked arguments are skipped
    because their behavior cannot be determined safely by this static rule.
    """
    tree = ast.parse(source)
    findings: list[tuple[int, int, str]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not _is_direct_open_call(node):
            continue
        if any(isinstance(argument, ast.Starred) for argument in node.args):
            continue
        if any(keyword.arg is None for keyword in node.keywords):
            continue
        if not _has_file_argument(node) or _has_explicit_encoding(node):
            continue
        if _text_mode(node) is not True:
            continue

        findings.append((node.lineno, node.col_offset, MISSING_ENCODING_MESSAGE))

    findings.sort(key=lambda finding: (finding[0], finding[1]))
    return [(line_number, message) for line_number, _, message in findings]
