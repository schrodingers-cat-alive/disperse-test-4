---
icon: lucide/frown
---

# Main documentation

`disperse` is a Python package for identifying modes of collective neutrino oscillations by solving their dispersion
relation. Collective neutrino oscillations occur in extreme, neutrino-dense astrophysical environments such as
core-collapse supernovae and neutron star mergers.  Currently, `disperse` solves the axisymmetric dispersion relation
defined by equations (2.17) to (2.19) in reference [^1], including Landau damping, without collisions, and currently
only for isotropic Gaussian neutrino distributions.

(Version 0.2.0 of `disperse` is not compatible with version 0.1.0.)

!!! note

    Please refresh this page if the LaTeX math is not displaying for you.

## Features

- Includes a flexible set of functions for carrying out calculations
- Implements Landau damping[^1][^2]
- Searches for solutions in succession, using the previous solution for the next initial guess (see
  [`shoot`](#disperse.rootfinding.shoot))
- Conservative/low false positive rate: Checks convergence of numerical integrals, floating-point error, etc., and
  returns NaN if tolerances aren't met
- Uses arbitrary-precision arithmetic to carry out numerically difficult calculations
- Takes advantage of analytical simplification that can be done in several special cases
- Can write results to data files as calculations are performed (partial results can be used if the
  calculation is interrupted)
- Open source!

## Conventions and terminology

The calculations carried out by `disperse` closely follow reference [^1], and so do the conventions and terminology that
its source code and documentation use. As in reference [^1]:

- "Neutrino distribution" refers to the "difference in lepton number" given by the difference in the diagonal
  elements of the density matrix/Wigner distribution. It is denoted by $G_{\mathbf{p}}$ and
  $- \overline{G}_{\mathbf{p}}$ in reference [^1].
- "Wavenumber" or "wavevector" without further qualification refers to the shifted wavenumber or wavevector of a
  mode, defined in section (2.1) of reference [^1].
- "Frequency" without further qualification refers to the shifted angular frequency of a mode.
- The letter $v$ denotes the component of neutrinos' velocities in the direction of the axis of symmetry. (The word
  "velocity" is sometimes used without further qualification to refer to this quantity as well.)

Furthermore:

- A "collective (neutrino) oscillation mode" refers to a mode of the off-diagonal elements (coherences) of the neutrino
  density matrix/Wigner distribution, i.e. a mode of the quantity denoted by $\psi_{\mathbf{p}}$ in reference [^1].
- The integrals defined by equation (2.17) of reference [^1], denoted $I_n$, are referred to as "Fiorillo integrals".
- The value of $n$ is referred to as the "kind" of Fiorillo integral.
    - The `"0_2"` kind of integral is also defined as the difference in integrals $I_0 - I_2$.
- The "vacuum-frequency-first" integration method refers to integration that properly handles branch cuts, as described
  in reference [^2], as opposed to the previous "velocity-first" integration method, which integrates along paths that
  may cross branch cuts.
- Vacuum frequency, instead of energy, is used to parameterize neutrino distributions and densities (e.g. DLN per vacuum
  frequency, instead of per energy).
- The neutrino flavor isospin convention is adopted (in which neutrinos and antineutrinos are treated on equal footing
  and as having vacuum frequencies of opposite signs).
- The neutrino-neutrino interaction scale $\mu$ is set to one.

## Assumptions

The current functionality implemented in `disperse` has the following assumptions or limitations.

- The assumptions used to derive equations (2.17) to (2.19) in reference [^1] are used, including the assumptions that:
    - The neutrino distribution is homogeneous, axisymmetric, and time-independent (it depends only on $v$ and the
      vacuum frequency).
    - The wavevector of the collective oscillation mode is directed along the axis of symmetry.
    - (As usual:) The dynamics include only neutrino-neutrino interactions and are governed by the quantum-kinetic
      equations in the mean-field limit and in the linear regime (mode-mode coupling is neglected), and there are only
      two relevant neutrino flavors.
- Collisions are ignored ($\Gamma_E = \overline{\Gamma}_E = 0$).
- Landau damping is always assumed for decaying modes whose frequencies have a negative imaginary part. Complex
  conjugate solutions of unstable modes will not be found.
- Currently, only isotropic multi-Gaussian neutrino distributions and the vacuum-frequency-first integration method are
  supported.

## API

Documentation on the individual modules and functions that make up `disperse` can be found below.

### ::: disperse.rootfinding
    options:
        show_root_heading: true
        show_source: true

### ::: disperse.residuals
    options:
        show_root_heading: true
        show_source: true

### ::: disperse.fiorillointegrals
    options:
        show_root_heading: true
        show_source: true

### ::: disperse.data
    options:
        show_root_heading: true
        show_source: true

### ::: disperse.mathematica
    options:
        show_root_heading: true
        show_source: true

### ::: disperse.saferscipy
    options:
        show_root_heading: true
        show_source: true

[^1]: Fiorillo and Raffelt, 2026. [arXiv:2505.20389](https://arxiv.org/abs/2505.20389)
[^2]: Kost and Duan, 2026. [arXiv:2603.22246](https://arxiv.org/abs/2603.22246)
