import src


def test_package_imports() -> None:
    assert src.__name__ == "src"
