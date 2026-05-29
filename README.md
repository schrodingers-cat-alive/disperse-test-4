A Python package for solving dispersion relations of collective neutrino oscillations.

Features:

- Includes a flexible set of functions for carrying out calculations
- Implements Landau damping[^1][^2]
- Can search for solutions in succession using the ["shooting" method](https://UNM-NuCO.github.io/disperse/main-documentation/#disperse.rootfinding.shoot)
- Conservative: Returns NaN if tolerances aren't met
- Uses arbitrary-precision arithmetic to carry out numerically difficult calculations
- Takes advantage of analytical simplification that can be done in several special cases
- Can write results to data files as calculations are performed
- Open source!

[Read the docs and get started here.](https://UNM-NuCO.github.io/disperse/)

[^1]: Fiorillo and Raffelt, 2024. [arXiv:2406.06708](https://arxiv.org/abs/2406.06708)
[^2]: Kost and Duan, 2026. [arXiv:2603.22246](https://arxiv.org/abs/2603.22246)
