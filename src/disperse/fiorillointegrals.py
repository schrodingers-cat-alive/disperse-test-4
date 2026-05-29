"""Functions that calculate "Fiorillo integrals".

Results of symbolic integrals as well as numerical integration are used in the
calculations. Symbolic integral results are evaluated using arbitrary-precision
arithmetic.
"""

import math
import scipy.special

from math import pi

from .mathematica import from_mathematica

from collections.abc import Callable, Collection, Mapping
from typing import Final

_ISOTROPIC_GAUSSIAN_MATHEMATICA_STRINGS: Final[Mapping[str, str]] = {
    "0": """
    ((-I)*Pi*(Erf[(K + u - W)/(Sqrt[2]*s)] + Erf[(K - u + W)/(Sqrt[2]*s)]) + 
   ((-(K + u - W)^2)*HypergeometricPFQ[{1, 1}, {3/2, 2}, 
       -((K + u - W)^2/(2*s^2))] + (K - u + W)^2*HypergeometricPFQ[{1, 1}, 
       {3/2, 2}, -((K - u + W)^2/(2*s^2))])/s^2)/(4*K) 
    """,
    "1": """
    -((I*(2*s^2*(-2*I*Sqrt[2]*K + (-E^(-((K + u - W)^2/(2*s^2))) + 
         E^(-((K - u + W)^2/(2*s^2))))*Sqrt[Pi]*s) + 
     I*(4*s^3*DawsonF[(K + u - W)/(Sqrt[2]*s)] + 
       4*s^3*DawsonF[(K - u + W)/(Sqrt[2]*s)] + Sqrt[2]*(u - W)*
        (Pi*s^2*(Erf[(K + u - W)/(Sqrt[2]*s)]*(I + Erfi[(K + u - W)/(Sqrt[2]*
                s)]) - Erf[(K - u + W)/(Sqrt[2]*s)]*
            (-I + Erfi[(K - u + W)/(Sqrt[2]*s)])) - (K + u - W)^2*
          HypergeometricPFQ[{1, 1}, {3/2, 2}, (K + u - W)^2/(2*s^2)] + 
         (K - u + W)^2*HypergeometricPFQ[{1, 1}, {3/2, 2}, 
           (K - u + W)^2/(2*s^2)]))))/(4*Sqrt[2]*K^2*s^2)) 
    """,
    "2": """
    (4*K*(u - W) + (I*Sqrt[2*Pi]*s*(K + u - W))/E^((K - u + W)^2/(2*s^2)) + 
   (I*Sqrt[2*Pi]*s*(K - u + W))/E^((K + u - W)^2/(2*s^2)) + 
   2*Sqrt[2]*s*(K - u + W)*DawsonF[(K + u - W)/(Sqrt[2]*s)] - 
   2*Sqrt[2]*s*(K + u - W)*DawsonF[(K - u + W)/(Sqrt[2]*s)] - 
   ((s^2 + (u - W)^2)*(Pi*s^2*(Erf[(K + u - W)/(Sqrt[2]*s)]*
         (I + Erfi[(K + u - W)/(Sqrt[2]*s)]) - Erf[(K - u + W)/(Sqrt[2]*s)]*
         (-I + Erfi[(K - u + W)/(Sqrt[2]*s)])) - 
      (K + u - W)^2*HypergeometricPFQ[{1, 1}, {3/2, 2}, 
        (K + u - W)^2/(2*s^2)] + (K - u + W)^2*HypergeometricPFQ[{1, 1}, 
        {3/2, 2}, (K - u + W)^2/(2*s^2)]))/s^2)/(4*K^3) 
    """,
    "0_2": """
    -((4*K*(u - W) + (I*Sqrt[2*Pi]*s*(K + u - W + E^((2*K*(-u + W))/s^2)*
        (K - u + W)))/E^((K - u + W)^2/(2*s^2)) + 2*Sqrt[2]*s*(K - u + W)*
     DawsonF[(K + u - W)/(Sqrt[2]*s)] - 2*Sqrt[2]*s*(K + u - W)*
     DawsonF[(K - u + W)/(Sqrt[2]*s)] - 
    ((-K^2 + s^2 + (u - W)^2)*(Pi*s^2*(Erf[(K + u - W)/(Sqrt[2]*s)]*
          (I + Erfi[(K + u - W)/(Sqrt[2]*s)]) - Erf[(K - u + W)/(Sqrt[2]*s)]*
          (-I + Erfi[(K - u + W)/(Sqrt[2]*s)])) - (K + u - W)^2*
        HypergeometricPFQ[{1, 1}, {3/2, 2}, (K + u - W)^2/(2*s^2)] + 
       (K - u + W)^2*HypergeometricPFQ[{1, 1}, {3/2, 2}, 
         (K - u + W)^2/(2*s^2)]))/s^2)/(4*K^3)) 
    """,
}
"""Mathematica expressions for Fiorillo integrals for isotropic Gaussian distributions.

Maps "kinds" of Fiorillo integrals to strings containing their analytically evaluated
form expressed in Mathematica InputForm.

An isotropic Gaussian distribution is equivalent to an isotropic multi-Gaussian
distribution with a single Gaussian with a normalization of one.

Variables in the expressions:
- K: Wavenumber of the mode.
- W: Angular frequency of the mode.
- u: Mean of the Gaussian.
- s: Standard deviation of the Gaussian.
"""


_ISOTROPIC_GAUSSIAN_FIORILLO: Final[
    Mapping[str, Callable[[float, complex, float, float], complex]]
] = {
    kind: from_mathematica(arguments=["K", "W", "u", "s"], string=string)
    for kind, string in _ISOTROPIC_GAUSSIAN_MATHEMATICA_STRINGS.items()
}
"""Fiorillo integrals for isotropic Gaussian distributions.

Maps "kinds" of integrals to functions that evaluate them. The functions are created
from the Mathematica expressions in `_isotropic_gaussian_mathematica_strings`.

An isotropic Gaussian distribution is equivalent to an isotropic multi-Gaussian
distribution with a single Gaussian with a normalization of one.
"""


def isotropic_multi_gaussian_fiorillo(
    wavenumber: float,
    frequency: complex,
    normalizations: Collection[float],
    means: Collection[float],
    widths: Collection[float],
    kind: str,
) -> complex:
    """Fiorillo integrals for isotropic multi-Gaussian distributions.

    Integrals are calculated using the complex vacuum frequency method.
    `normalizations`, `means`, and `widths` must have the same length.

    An isotropic multi-Gaussian distribution is a neutrino distribution with no
    dependence on velocity and a dependence on vacuum frequency given by the sum of
    multiple Gaussians with arbitrary normalizations, means, and standard deviations
    (widths).

    Args:
        wavenumber: Wavenumber of the collective mode.
        frequency: Angular frequency of the collective mode.
        normalizations: Normalizations of the Gaussians.
        means: Means of the Gaussians.
        widths: Standard deviations of the Gaussians.
        kind: The kind of Fiorillo integral. Can be `'0'`, `'1'`, `'2'`, or `'0_2'`.
    """
    if not len(normalizations) == len(means) == len(widths):
        raise ValueError(
            "Normalizations, means, and widths should all have the same length."
        )

    fiorillo = _ISOTROPIC_GAUSSIAN_FIORILLO[kind]

    # Multiply the Fiorillo integral for each individual Gaussian by its normalization
    # and then sum them together.
    return sum(
        normalization * fiorillo(wavenumber, frequency, mean, width)
        for normalization, mean, width in zip(normalizations, means, widths)
    )


def homogeneous_isotropic_gaussian_fiorillo(
    frequency: complex, kind: str | complex
) -> complex:
    """Fiorillo integrals for homogeneous modes in an isotropic Gaussian distribution.

    The Gaussian is normalized, has zero mean, and has a width of 1.

    Args:
        frequency: Angular frequency of the collective mode.
        kind: The kind of Fiorillo integral. Can be any complex number or string
            representation of one (typically the integers 0, 1, or 2), or `'0_2'`.
    """
    if kind == "0_2":
        factor = 2 / 3
    else:
        n = complex(kind)
        factor = (1 - (-1) ** (n + 1)) / (2 * (n + 1))

    return -1j * math.sqrt(pi / 2) * faddeeva(frequency / math.sqrt(2)) * factor


def faddeeva(z: complex) -> complex:
    """Faddeeva function for built-in Python numbers.

    This is a wrapper around `scipy.special.wofz` that returns a built-in Python
    `complex` number instead of a NumPy scalar.
    """
    return scipy.special.wofz(z).item()
