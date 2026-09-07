"""Tests for the squared-error example calculation."""

from viz.calculations import squared_error


def test_example_squared_error() -> None:
    assert squared_error(7, 5) == 4


def test_negative_error_is_squared() -> None:
    assert squared_error(3, 5) == 4


def test_matching_values_have_zero_error() -> None:
    assert squared_error(5, 5) == 0
