"""Tools for solving equations by finding the roots of their residuals."""

import numpy as np

from .saferscipy import safer_root

from typing import Any, TypeVar
from collections.abc import Callable, Iterable
from numpy import float64
from numpy.typing import ArrayLike, NDArray

T = TypeVar("T")

residual_tolerance: float = 1e-6
"""The tolerance for the size of the residual used by `safer_root` and `shoot`."""


def shoot(
    residual: Callable[[NDArray[float64], T], ArrayLike],
    parameter_values: Iterable[T],
    first_guess: ArrayLike,
    root_dataset: Any = None,
    parameter_dataset: Any = None,
) -> NDArray[float64]:
    """Find roots in succession while varying parameters of the residual.

    In each iteration, the most recent root that was found successfully is used as the
    initial guess for the next root (unless no roots have been found successfully yet,
    in which case the `first_guess` is used).

    TODO: Use `logging` instead of `print`.

    Args:
        residual: Roots in `x` of `residual(x, *parameter_values_)` are searched for,
            with each set of `parameter_values_` taken in succesion from the
            `parameter_values` argument. Since `scipy.optimize.root` is used for root
            finding, `x` and the value that `residual` returns may be 1D NumPy arrays,
            and each set of `parameter_values_` may be a single parameter or a tuple.
        parameter_values: An iterable of parameter values (each a single parameter or a
            tuple, as `scipy.optimize.root` accepts) that specify the specific residuals
            in the order in which their roots will be searched for.
        first_guess: The initial guess for the root-finding algorithm for the first
            root(s) that are searched for.
        root_dataset: An optional dataset to save roots to while they are being found.
            Should support indexed assignment as in `root_dataset[i] = root`.
        parameter_dataset: Like `root_dataset`, but for the parameter values. Should
            support indexed assignment as in `parameter_dataset[i] = parameter_values_`.

    Returns:
        An array of roots.
    """
    roots = []

    guess = first_guess

    for i, parameter_values_ in enumerate(parameter_values):
        root = safer_root(residual_tolerance, residual, guess, parameter_values_)

        if root_dataset is not None:
            root_dataset[i] = root

        if parameter_dataset is not None:
            parameter_dataset[i] = parameter_values_

        if np.isfinite(root).all():
            guess = root

            print(f"Found a root! {root}    With these parameters: {parameter_values_}")
        else:
            print(
                f":( could not find a root with these parameters: {parameter_values_}"
            )

        roots.append(root)

    return np.array(roots)
