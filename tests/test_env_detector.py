"""Tests for platform-specific environment variable detection."""

import pytest

from portabilityguard.env_detector import find_platform_specific_env_vars


@pytest.mark.parametrize("variable", ["APPDATA", "LOCALAPPDATA"])
def test_detects_windows_variable_without_host_value(
    variable: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(variable, raising=False)
    source = f'import os\ncache = os.environ["{variable}"]\n'

    assert find_platform_specific_env_vars(source) == [(2, variable)]


def test_reports_line_where_multiline_access_starts() -> None:
    source = 'cache = (\n    os.environ[\n        "APPDATA"\n    ]\n)\n'

    assert find_platform_specific_env_vars(source) == [(2, "APPDATA")]


def test_returns_multiple_reads_in_source_order() -> None:
    source = (
        'paths = (str(os.environ["LOCALAPPDATA"]), os.environ["APPDATA"])\n'
        "\n"
        'cache = os.environ["APPDATA"]\n'
    )

    assert find_platform_specific_env_vars(source) == [
        (1, "LOCALAPPDATA"),
        (1, "APPDATA"),
        (3, "APPDATA"),
    ]


@pytest.mark.parametrize(
    "source",
    [
        'os.environ.get("APPDATA", "/tmp")',
        'os.environ.get("LOCALAPPDATA", "fallback")',
        'os.environ["HOME"]',
        'os.environ["USERPROFILE"]',
        '# os.environ["APPDATA"]',
        "'os.environ[\"LOCALAPPDATA\"]'",
        'os.environ["APP" + "DATA"]',
        'key = "APPDATA"\nos.environ[key]',
        'os.environ[f"LOCAL{suffix}"]',
        'settings.environ["APPDATA"]',
        'import os as operating_system\noperating_system.environ["APPDATA"]',
        'os.environ["APPDATA"] = "/tmp"',
    ],
)
def test_ignores_expressions_outside_the_rule(source: str) -> None:
    assert find_platform_specific_env_vars(source) == []


def test_does_not_execute_source() -> None:
    source = 'raise RuntimeError("must not run")\ncache = os.environ["APPDATA"]\n'

    assert find_platform_specific_env_vars(source) == [(2, "APPDATA")]
