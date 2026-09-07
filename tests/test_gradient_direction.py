"""Tests for the gradient-direction teaching example."""

from viz.calculations import gradient_descent_step, weight_gradient


def test_gradient_sign_on_each_side_of_minimum() -> None:
    assert weight_gradient(7) > 0
    assert weight_gradient(3) < 0
    assert weight_gradient(5) == 0


def test_descent_moves_toward_minimum_from_each_side() -> None:
    assert gradient_descent_step(7) < 7
    assert gradient_descent_step(3) > 3
