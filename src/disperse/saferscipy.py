"""Wrappers of SciPy functions that simply return NaN when things go wrong."""

import numpy as np
import scipy.optimize

from typing import Any
from numpy import float64
from numpy.typing import NDArray


def safer_root(tolerance: float, *args: Any, **kwargs: Any) -> NDArray[float64]:
    """Search for a root, but return NaN if numerical issues are detected.

    Uses `scipy.optimize.root` for root finding. If `scipy.optimize.root` reports that
    the algorithm failed, or if the absolute value of the residual (or the largest
    component of the residual) evaluated at the solution that it finds is greater than
    `tolerance`, an array of NaNs is returned instead of the solution.

    TODO: Consider not checking whether the algorithm reports a failure, since checking
        the size of the residual is *probably* good enough.

    Args:
        tolerance: If the absolute value of the residual (or the largest component of
            the residual) evaluated at the solution that is found is greater than this
            tolerance, return NaNs instead of the solution.
        *args: Positional arguments passed to `scipy.optimize.root`.
        **kwargs: Keyword arguments passed to `scipy.optimize.root`.

    Returns:
        The root or NaNs.
    """
    results = scipy.optimize.root(*args, **kwargs)

    if not results.success or abs(results.fun).max() > tolerance:
        return np.full_like(results.x, np.nan)

    return results.x
