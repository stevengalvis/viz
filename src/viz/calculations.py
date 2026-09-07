"""Small, rendering-independent calculations used by the scenes."""


def squared_error(prediction: float, target: float) -> float:
    """Return the squared error for one prediction and target."""

    error = prediction - target
    return error**2
