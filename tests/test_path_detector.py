"""Tests for absolute path detection."""

from portabilityguard.path_detector import find_absolute_paths, is_absolute_path


def test_is_absolute_path_recognizes_linux_and_macos_paths() -> None:
    assert is_absolute_path("/home/alice/project/config.json")
    assert is_absolute_path("/Users/Alice/project/config.json")


def test_is_absolute_path_recognizes_windows_path() -> None:
    assert is_absolute_path(r"C:\Users\Alice\data.csv")


def test_is_absolute_path_rejects_relative_paths() -> None:
    assert not is_absolute_path("./config.json")
    assert not is_absolute_path("data/input.csv")


def test_find_absolute_paths_detects_posix_literal() -> None:
    source = 'config = "/home/alice/project/config.json"\n'

    assert find_absolute_paths(source) == [(1, "/home/alice/project/config.json")]


def test_find_absolute_paths_detects_windows_literal_on_any_host() -> None:
    source = r'data = r"C:\Users\Alice\data.csv"'

    assert find_absolute_paths(source) == [(1, r"C:\Users\Alice\data.csv")]


def test_find_absolute_paths_ignores_relative_literals() -> None:
    source = 'config = "./config.json"\ndata = "data/input.csv"\n'

    assert find_absolute_paths(source) == []


def test_find_absolute_paths_returns_multiple_paths_and_line_numbers() -> None:
    source = (
        'relative = "data/input.csv"\n'
        'posix = "/var/log/app.log"\n'
        "\n"
        r'windows = r"D:\Reports\annual.csv"'
        "\n"
    )

    assert find_absolute_paths(source) == [
        (2, "/var/log/app.log"),
        (4, r"D:\Reports\annual.csv"),
    ]


def test_find_absolute_paths_does_not_execute_source() -> None:
    source = 'raise RuntimeError("must not run")\npath = "/etc/hosts"\n'

    assert find_absolute_paths(source) == [(2, "/etc/hosts")]
