"""Residual functions that define dispersion relation equations.

All of the residuals in this module use the assumption that the neutrino distribution is
axisymmetric.

TODO: Don't forget to add checks on the sizes of inputs when they become necessary.
    Document them too.
"""

from functools import wraps

from typing import Any, Callable


def realify(function: Callable[..., complex]) -> Callable[..., tuple[float, float]]:
    """Wrap a function to handle complex numbers as real arrays/tuples of length 2.

    Args:
        function: A function that should take a complex number as its first argument and
            return a complex number (scalar).

    Returns:
        A function that takes a real array of length 2 as its first argument and
            returns a similarly shaped array (a tuple containing 2 items).
    """

    @wraps(function)
    def new_function(array_input, *args, **kwargs):
        complex_input = array_input[0] + 1j * array_input[1]
        complex_output = function(complex_input, *args, **kwargs)
        array_output = (complex_output.real, complex_output.imag)

        return array_output

    return new_function


def transverse_residual(fiorillo_0_2: Any) -> Any:
    """Dispersion relation for transverse modes in terms of the difference $I_0 - I_2$.

    Equivalent to (the left-hand side of) equation (2.18) in reference [^1].

    [^1]: Fiorillo and Raffelt, 2026. [arXiv:2505.20389](https://arxiv.org/abs/2505.20389)

    Args:
        fiorillo_0_2: The difference in Fiorillo integrals $I_0 - I_2$.
    """
    return fiorillo_0_2 + 2
