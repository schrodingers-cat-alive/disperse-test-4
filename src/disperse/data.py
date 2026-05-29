"""Tools for saving dispersion relation data."""

from datetime import datetime
from pathlib import Path

import netCDF4
import xarray
import numpy as np

from typing import Any

import os


def get_timestamp() -> str:
    """Get a timestamp representing the current time."""
    return datetime.now().isoformat().replace(":", "-").replace(".", "-")


def create_frequency_dataset(
    folder: str | os.PathLike[str],
    dimension_name: str,
    dataset_name: str = "",
    attrs: dict[str, Any] = dict(),
) -> netCDF4.Dataset:
    """Create an empty dataset for complex frequencies that vary along one dimension.

    Creates a `netCDF4.Dataset` dataset with one dimension of the given `dimension_name`
    and one dimension named `"ri"` with coordinates `"r"` and `"i"` for specifying the
    real and imaginary parts of the frequencies. The former dimension is an unlimited
    dimension that can be written to in a sequential manner, e.g., while calculations
    are being performed.

    Note: Returns an *open* `netCDF4.Dataset` dataset in the specified `folder`.
        (The dataset and its file can be closed by calling its `close` method.)

    TODO: Remove dependence on `xarray` and build the dataset entirely using the
        `netCDF4` package.

    Args:
        folder: Create the dataset in the folder at this path.
        dimension_name: Name of the single dimension along which the frequency varies.
        dataset_name: Optional name for the dataset.
        attrs: Optional dictionary specifying attributes of the dataset.

    Returns:
        The open `netCDF4.Dataset` dataset.
    """
    timestamp = get_timestamp()

    if dataset_name == "":
        filename = f"{timestamp}.nc"
        dataset_name = "None"
    else:
        filename = f"{dataset_name}-{timestamp}.nc"

    attrs = {"dataset_name": dataset_name, **attrs}

    # Create the (empty) dataset in memory using Xarray, which has a more convenient
    # interface than `netCDF4`.
    dataset = xarray.Dataset(
        data_vars={"frequency": ((dimension_name, "ri"), np.empty((0, 2)))},
        coords={dimension_name: (dimension_name, []), "ri": ("ri", ["r", "i"])},
        attrs=attrs,
    )

    folder = Path(folder)
    path = folder / filename

    # Save the Xarray dataset as a netCDF file and then reopen it as a `netCDF4.Dataset`
    # dataset so it can be written to in a sequential manner.
    dataset.to_netcdf(path, unlimited_dims=dimension_name)
    dataset = netCDF4.Dataset(path, "a")

    return dataset
