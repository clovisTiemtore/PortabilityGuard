"""Tests for missing encoding detection."""

import pytest

from portabilityguard.encoding_detector import (
    MISSING_ENCODING_MESSAGE,
    find_missing_encodings,
)


@pytest.mark.parametrize("mode", ["r", "w", "a", "x", "rt", "r+"])
def test_find_missing_encodings_detects_text_modes(mode: str) -> None:
    source = f'open("file.txt", "{mode}")\n'

    assert find_missing_encodings(source) == [(1, MISSING_ENCODING_MESSAGE)]


def test_find_missing_encodings_detects_default_mode() -> None:
    source = 'open("file.txt")\n'

    assert find_missing_encodings(source) == [(1, MISSING_ENCODING_MESSAGE)]


def test_find_missing_encodings_detects_keyword_mode() -> None:
    source = 'open("file.txt", mode="w")\n'

    assert find_missing_encodings(source) == [(1, MISSING_ENCODING_MESSAGE)]


@pytest.mark.parametrize("mode", ["rb", "wb", "ab", "xb", "r+b"])
def test_find_missing_encodings_ignores_binary_modes(mode: str) -> None:
    source = f'open("file.bin", "{mode}")\n'

    assert find_missing_encodings(source) == []


def test_find_missing_encodings_ignores_binary_keyword_mode() -> None:
    source = 'open("file.bin", mode="wb")\n'

    assert find_missing_encodings(source) == []


@pytest.mark.parametrize(
    "source",
    [
        'open("file.txt", encoding="utf-8")\n',
        'open("file.txt", "r", encoding="utf-8")\n',
        'open("file.txt", "r", -1, "utf-8")\n',
        'open(file="file.txt", mode="w", encoding=selected_encoding)\n',
    ],
)
def test_find_missing_encodings_ignores_explicit_encoding(source: str) -> None:
    assert find_missing_encodings(source) == []


def test_find_missing_encodings_returns_multiple_findings_and_line_numbers() -> None:
    source = (
        'open("first.txt")\n'
        'open("binary.bin", "rb")\n'
        "\n"
        'open("second.txt", mode="a")\n'
    )

    assert find_missing_encodings(source) == [
        (1, MISSING_ENCODING_MESSAGE),
        (4, MISSING_ENCODING_MESSAGE),
    ]


def test_find_missing_encodings_ignores_code_without_problems() -> None:
    source = (
        'with open("input.txt", encoding="utf-8") as input_file:\n'
        "    content = input_file.read()\n"
        'with open("output.bin", "wb") as output_file:\n'
        '    output_file.write(b"data")\n'
    )

    assert find_missing_encodings(source) == []


def test_find_missing_encodings_ignores_comments_and_strings() -> None:
    source = (
        '# open("comment.txt")\n'
        "example = 'open(\"string.txt\")'\n"
        'description = "Call open() safely"\n'
    )

    assert find_missing_encodings(source) == []


@pytest.mark.parametrize(
    "source",
    [
        'open("file.txt", mode)\n',
        'open("file.txt", mode=get_mode())\n',
        'open("file.txt", *options)\n',
        'open("file.txt", **options)\n',
    ],
)
def test_find_missing_encodings_ignores_indeterminate_arguments(source: str) -> None:
    assert find_missing_encodings(source) == []


def test_find_missing_encodings_does_not_report_other_open_methods() -> None:
    source = 'path.open("r")\nopener.open("file.txt")\n'

    assert find_missing_encodings(source) == []


def test_find_missing_encodings_ignores_invalid_calls_and_modes() -> None:
    source = (
        "open()\n" 'open("file.txt", "invalid")\n' 'open("file.txt", "r", mode="w")\n'
    )

    assert find_missing_encodings(source) == []
