"""Smoke tests for the top-level package."""


def test_viz_imports() -> None:
    import viz

    assert viz.__version__ == "0.1.0"
