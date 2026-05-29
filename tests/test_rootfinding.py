import numpy as np
from numpy.testing import assert_allclose

from disperse.rootfinding import shoot


def test_shoot():
    """A simple, non-comprehensive test of `shoot`.

    Although not comprehensive, this test checks if roots may be found after previous
    roots were failed to be found.
    """
    actual = shoot(
        lambda x, y: -(x**2) - y,
        [4, 1, 0, -1, -4, -9],
        -1,
    )

    desired = np.array(
        [
            [np.nan],
            [np.nan],
            [np.nan],
            [-1.0],
            [-2.0],
            [-3.0],
        ]
    )

    assert_allclose(actual, desired, equal_nan=True)
