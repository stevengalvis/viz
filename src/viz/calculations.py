"""Small, rendering-independent calculations used by the scenes."""


def squared_error(prediction: float, target: float) -> float:
    """Return the squared error for one prediction and target."""

    error = prediction - target
    return error**2


def weight_loss(weight: float) -> float:
    """Return the one-dimensional loss whose minimum is at weight five."""

    return (weight - 5) ** 2


def weight_gradient(weight: float) -> float:
    """Return the derivative of :func:`weight_loss` at ``weight``."""

    return 2 * (weight - 5)


def gradient_descent_step(weight: float, learning_rate: float = 0.1) -> float:
    """Take one gradient-descent step for the one-dimensional loss."""

    return weight - learning_rate * weight_gradient(weight)
