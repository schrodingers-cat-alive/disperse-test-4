# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "disperse",
#     "marimo>=0.23.8",
#     "matplotlib==3.10.9",
#     "numpy==2.4.6",
#     "python-flint>=0.8.0",
#     "xarray==2026.4.0",
# ]
#
# [tool.uv.sources]
# disperse = { path = "../" }
# ///

import marimo

__generated_with = "0.23.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Example demonstrating usage of the `disperse` package.

    You should be able to edit, add, and (re)run cells in this marimo notebook right now. You can also hover over functions, etc., to see some of their documentation.

    This notebook solves for a few branches of the dispersion relation of transverse (axial symmetry-breaking) collective oscillation modes in an isotropic Gaussian neutrino distribution (a neutrino distribution that is isotropic and has a Gaussian shape in vacuum frequency).
    """)
    return


@app.cell(hide_code=True)
def _():
    # Micropip is only necessary to make this notebook work in web browsers.
    import micropip

    return (micropip,)


@app.cell(hide_code=True)
async def _(micropip):
    await micropip.install("../../disperse-0.2.0-py3-none-any.whl")
    return


@app.cell
def _():
    from pathlib import Path

    import numpy as np
    import matplotlib.pyplot as plt
    import xarray as xr

    from flint import ctx

    from disperse.fiorillointegrals import isotropic_multi_gaussian_fiorillo
    from disperse.residuals import realify, transverse_residual
    from disperse.rootfinding import shoot, safer_root
    from disperse.data import create_frequency_dataset

    return (
        Path,
        create_frequency_dataset,
        ctx,
        isotropic_multi_gaussian_fiorillo,
        np,
        plt,
        realify,
        safer_root,
        shoot,
        transverse_residual,
        xr,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Settings
    """)
    return


@app.cell
def _(Path, ctx):
    # Set the precision for arithmetic done by `flint`, in terms of decimal places.
    # (If the precision is too low, calculations may return NaN.)
    ctx.dps = 100

    # Set the width of the Gaussian.
    width = 1

    # Set the folder to save output to.
    folder = ""

    folder = Path(folder)
    return folder, width


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Define the residual function

    The dispersion relation is defined by setting the residual to 0. `realify` converts the residual's inputs and outputs from complex numbers to real arrays of length 2.
    """)
    return


@app.cell
def _(isotropic_multi_gaussian_fiorillo, realify, transverse_residual, width):
    normalization = 1
    mean = 0

    @realify
    def residual(frequency, wavenumber):
        return transverse_residual(isotropic_multi_gaussian_fiorillo(wavenumber, frequency, [normalization], [mean], [width], "0_2"))

    return (residual,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Search for frequencies at $K = 0$

    Below, we try out five values for the `_initial_frequency` - the initial guess for root finding. It is a list of the form `[real_part, imaginary_part]`. The first guess, `[0, 0]`, leads the root finder to find the solution `[-1.14429751 -1.22951544]`. The next guess, `[-1, 1]`, leads to the same solution. The next guess leads to no solution being found, and the fourth and fifth guesses lead to two new solutions, for a total of three distinct solutions.
    """)
    return


@app.cell
def _(residual, safer_root):
    # Use a small but nonzero wavenumber.
    wavenumber = 1e-3

    # `safer_root` returns NaN if it can't find a residual value smaller than this.
    residual_tolerance = 1e-8

    _initial_frequency = [0, 0]
    print(safer_root(residual_tolerance, residual, _initial_frequency, wavenumber))

    _initial_frequency = [-1, -1]
    print(safer_root(residual_tolerance, residual, _initial_frequency, wavenumber))

    _initial_frequency = [-5, -5]
    print(safer_root(residual_tolerance, residual, _initial_frequency, wavenumber))

    _initial_frequency = [-10, -10]
    print(safer_root(residual_tolerance, residual, _initial_frequency, wavenumber))

    _initial_frequency = [10, -10]
    print(safer_root(residual_tolerance, residual, _initial_frequency, wavenumber))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # "Shoot" for branches of the dispersion relation ($K \geq 0$)

    (This may take several seconds to run.)

    What we refer to as the "shooting" method is the process of searching for solutions to an equation in succession as a parameter of the equation is varied, using the most recent solution found as the initial guess for the next solution. We will search for frequencies as the wavenumber is varied.

    The shooting method requires a single initial guess as input. Below, we run it three times, each time starting at a wavenumber near zero and using one of three initial guesses for frequency that led us to find distinct solutions (for a wavenumber near zero) above.
    """)
    return


@app.cell
def _(create_frequency_dataset, folder, np, residual, shoot):
    # The (common) wavenumbers of the branches, starting near zero.
    wavenumbers = np.linspace(1e-3, 5, 10)

    # Initial frequencies we found before that led the root finder to distinct solutions at a wavenumber near zero.
    initial_frequencies = ([0, 0], [-10, -10], [10, -10])

    dataset_name = "example"

    for _initial_frequency in initial_frequencies:
        # Create a dataset file.
        _dataset = create_frequency_dataset(folder, "wavenumber", dataset_name, {"initial_frequency": _initial_frequency})

        # Calculate the frequencies using the "shooting" method and simultaneously write them to the file.
        shoot(residual, wavenumbers, _initial_frequency, _dataset["frequency"], _dataset["wavenumber"])

        _dataset.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Plot the branches
    """)
    return


@app.cell
def _(folder, plt, width, xr):
    # Load all of the dataset files using Xarray.
    datasets = [xr.open_dataset(path) for path in folder.glob("*.nc")]

    fig, ax = plt.subplots(2, 1, figsize=(5, 6), sharex=True)

    for _dataset in datasets:
        # Plot Re(frequency) vs. wavenumber.
        ax[0].plot(_dataset.wavenumber, _dataset.frequency.loc[:, "r"])

        # Plot Im(frequency) vs. wavenumber.
        ax[1].plot(_dataset.wavenumber, _dataset.frequency.loc[:, "i"])

    lw = 0.5

    # Plot light cones in the top panel.
    ax[0].axline([0, 0], [1, 1], lw=lw)
    ax[0].axline([0, 0], [1, -1], lw=lw)

    # Plot the Im(frequency) = 0 line in the bottom panel.
    ax[1].axhline(0, lw=lw)

    ax[0].set_title(rf"Isotropic Gaussian DR, width$ = {width}$")
    ax[1].set_xlabel(r"Wavenumber")
    ax[0].set_ylabel(r"Frequency - real part")
    ax[1].set_ylabel(r"Frequency - imaginary part")

    fig.tight_layout()
    fig.subplots_adjust(hspace=0)

    fig
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
