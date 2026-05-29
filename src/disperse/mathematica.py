"""Parse and evaluate Mathematica expressions using arbitrary-precision arithmetic.

Arbitrary-precision arithmetic is done using mpmath or python-flint.
"""

from functools import wraps

import flint
import mpmath
import sympy
import sympy.parsing.mathematica
import numpy as np

from collections.abc import Callable, Mapping
from typing import Any, Final

flint_absolute_tolerance: float = 1e-6
"""Absolute tolerance for the ball radius that decides when NaN is returned.

For calculations using python-flint.
"""

flint_relative_tolerance: float = 1e-6
"""Relative tolerance for the ball radius that decides when NaN is returned.

For calculations using python-flint.
"""

_DEFAULT_APA_LIBRARY: Final[str] = "flint"
"""The default arbitrary-precision arithmetic library to use.

(Currently, all Fiorillo integral calculations are hard-coded to choose the default
library.)
"""

# Set the default mpmath precision (number of decimal places).
mpmath.mp.dps = 100

# Set the default flint precision (number of decimal places).
flint.ctx.dps = 100


def from_mathematica(
    arguments: list[str], string: str, apa_library: str = _DEFAULT_APA_LIBRARY
) -> Callable[..., complex]:
    """Create a Python function from a Mathematica expression.

    The function that is created will convert its arguments to arbitrary-precision
    numbers for calculations and then convert the final result to a built-in `complex`
    number.

    Args:
        arguments: Specifies the signature of the function that is returned. Passed to
            the `args` parameter of `sympy.lambdify`.
        string: The Mathematica expression as a string. Can be Mathematica InputForm.
            Passed to `sympy.parsing.mathematica.parse_mathematica`.
        apa_library: The library to use to carry out aribtrary-precision arithmetic.
            Can be `'flint'` or `'mpmath'`. The default is `flint`.
    """
    if apa_library not in _APA_HELPERS.keys():
        raise ValueError(
            f"Sorry, the arbitrary-precision arithmetic library '{apa_library}' is not "
            f"supported. The only supported libraries are: {list(_APA_HELPERS.keys())}."
        )

    apa_helper = _APA_HELPERS[apa_library]

    # When `'Pi'` appears in the Mathematica expression, convert it to a function,
    # which is sometimes necessary in arbitrary-precision arithmetic (e.g. using
    # python-flint), because when the precision of calculations is increased, the
    # precision of `'Pi'` should increase accordingly as well.
    # Specifically, `'Pi'` is replaced with `'GetPi[0]'` (the argument of 0 does nothing
    # but is necessary since `sympy.parsing.mathematica.parse_mathematica` cannot parse
    # functions in this form with zero arguments). It follows that the modules passed to
    # `sympy.lambdify` should define `'GetPi'` as a callable function.
    string = string.replace("Pi", "GetPi[0]")

    expression = sympy.parsing.mathematica.parse_mathematica(string)

    function = sympy.lambdify(
        arguments,
        expression,
        modules=apa_helper.modules,
        cse=True,
    )

    function = apa_helper.make_types_safe(function)

    return function


class _APAHelper:
    """Class that helps with use of arbitrary-precision arithmetic libraries.

    Note: NumPy and SciPy functions typically* are either compatible with
    arbitrary-precision number types, calling their methods to ensure their types and
    precision are maintained, or they raise an error. Standard library `math` and `cmath`
    functions, however, convert their arguments to built-in Python `float` or `complex`
    values and can lose precision.

    * "typically" means that I haven't found any exceptions myself yet.

    Second note: In arbitrary-precision arithmetic, pi may need to be a function - so
    that when the precision of calculations is changed, the precision of pi changes,
    accordingly! (`from_mathematica` expects the modules that it passes to
    `sympy.lambdify` to define `'GetPi'` as a callable function, which takes one
    argument that does nothing and returns the value of $\pi$ with sufficient
    precision.)

    Third note: Including the `'mpmath'` module and also a custom module that redefines
    the `'mpf'` function (and possibly also `'mpc'`) lets `sympy.lambdify` call the
    custom function on numerical values (integers, reals, etc.) in lambdified
    expressions, so that precision isn't lost by doing arithmetic on built-in numerical
    values (e.g. 1 / 10).

    Attributes:
        lambdify_modules: Modules for passing to `sympy.lambdify`.
        to_ap_real: A function that should convert built-in Python floats to
            arbitrary-precision reals/floats.
        to_ap_complex: A function that should convert numbers to arbitrary-precision
            complex numbers.
        to_built_in_complex: A function that should convert arbitrary-precision numbers
            to built-in complex numbers. It may also check that the conversion is safe,
            e.g. it can return NaN if the error in the arbitrary-precision number is too
            large.
    """

    def __init__(
        self,
        lambdify_modules: Any,
        to_ap_real: Callable[[float], Any],
        to_ap_complex: Callable[[complex], Any],
        to_built_in_complex: Callable[[Any], complex],
    ):
        """Create an instance of an arbitrary-precision arithmetic helper.

        See the class documentation for descriptions of arguments.
        """
        self.modules = lambdify_modules
        self.to_ap_real = to_ap_real
        self.to_ap_complex = to_ap_complex
        self.to_built_in_complex = to_built_in_complex

    def to_ap_number(self, number: float | complex) -> Any:
        """Convert a number to an arbitrary-precision number.

        The returned arbitrary-precision number will be of real type if the number has
        zero imaginary part, and will be of complex type otherwise.
        """
        if number.imag == 0:
            return self.to_ap_real(number.real)

        return self.to_ap_complex(number)

    def make_types_safe(self, function: Callable[..., Any]) -> Callable[..., complex]:
        """Wrap a function so it handles input and output types in a safe way.

        The new function will explicitly "opt in" to arbitrary-precision arithmetic at
        the beginning by converting its inputs to arbitrary-precision numbers, and then
        explicitly "opt out" of arbitrary-precision arithmetic at the end by converting
        its output to a built-in Python `complex` number.
        """

        @wraps(function)
        def new_function(*args):
            args = [self.to_ap_number(arg) for arg in args]

            return self.to_built_in_complex(function(*args))

        return new_function


def _mpmath_dawson(x: mpmath.mpf | mpmath.mpc) -> mpmath.mpf | mpmath.mpc:
    """The Dawson function $D_+(x)$ using `mpmath`.

    CAUTION: If `x` is not already an `mpmath` number, this function's use of `x**2` may
    use lower precision arithmetic and lead to loss of the additional precision that
    `mpmath` provides.
    """
    return mpmath.sqrt(mpmath.pi) / 2 * mpmath.exp(-(x**2)) * mpmath.erfi(x)


def _flint_dawson(x: flint.arb | flint.acb) -> flint.arb | flint.acb:
    """The Dawson function $D_+(x)$ using `flint`.

    CAUTION: If `x` is not already a `flint` number, this function's use of methods of
    `x` may use lower precision arithmetic and lead to loss of the additional precision
    that `flint` provides.
    """
    return flint.arb.pi().sqrt() / 2 * (-(x**2)).exp() * x.erfi()


def _flint_to_built_in_complex(x: flint.arb | flint.acb) -> complex:
    """Convert a flint arbitrary-precision number to a built-in complex number.

    Returns NaN if the "ball radius" (error) in the arbitrary-precision number is too
    large.
    """
    if x.rad() > max(
        flint_absolute_tolerance, flint_relative_tolerance * x.abs_lower()
    ):
        return np.nan

    return complex(x)


_APA_HELPERS: Final[Mapping[str, _APAHelper]] = {
    "mpmath": _APAHelper(
        lambdify_modules=[
            "mpmath",
            {
                "Erf": mpmath.erf,
                "Erfi": mpmath.erfi,
                "HypergeometricPFQ": mpmath.hyper,
                "DawsonF": _mpmath_dawson,
                "GetPi": lambda _: mpmath.pi,
            },
        ],
        to_ap_real=mpmath.mpf,
        to_ap_complex=mpmath.mpc,
        to_built_in_complex=complex,
    ),
    "flint": _APAHelper(
        lambdify_modules=[
            {
                "mpf": flint.arb,
                "mpc": flint.acb,
            },
            {
                "Erf": lambda x: x.erf(),
                "Erfi": lambda x: x.erfi(),
                "HypergeometricPFQ": lambda a, b, x: x.hypgeom(a, b),
                "DawsonF": _flint_dawson,
                "GetPi": lambda _: flint.acb.pi(),
                # `sympy.lambdify` may pass built-in `int`s to the sqrt function, so
                # they need to be converted to `flint.acb` numbers.
                "sqrt": lambda x: flint.acb(x).sqrt(),
                "exp": lambda x: x.exp(),
            },
            "mpmath",
            "numpy",
            "scipy",
        ],
        # When using `flint`, convert all numbers to `flint.acb` type.
        to_ap_real=flint.acb,
        to_ap_complex=flint.acb,
        to_built_in_complex=_flint_to_built_in_complex,
    ),
}
"""Helpers for using mpmath and python-flint. See the `_APAHelper` class for more
information.
"""
