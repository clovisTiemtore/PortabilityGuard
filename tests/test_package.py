from importlib import import_module


def test_package_is_importable():
    assert import_module("portabilityguard").__name__ == "portabilityguard"
