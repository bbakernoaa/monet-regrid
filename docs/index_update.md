# monet-regrid: Regridding utilities for xarray

|PyPI| |DOI|

## Overview

"""
This file is part of monet-regrid.

monet-regrid is a derivative work of xarray-regrid.
Original work Copyright (c) 2023-2025 Bart Schilperoort, Yang Liu.
This derivative work Copyright (c) 2025 [Your Organization].

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Modifications: Package renamed from xarray-regrid to monet-regrid,
URLs updated, and documentation adapted for new branding.
"""

``monet-regrid`` extends xarray with regridding methods, making it possible to easily and efficiently regrid between rectilinear and curvilinear grids.

The new `build_regridder` factory API automatically detects grid types and dispatches to the appropriate regridder implementation. This ensures seamless handling of both rectilinear and curvilinear grids.

The following methods are supported:

*   `Linear <#>`_ (bilinear, or higher dimensional linear interpolation)
*   `Nearest-neighbor <#>`_
*   `Cubic <#>`_
*   `Conservative <#>`_
*   `Zonal statistics <#>`_ (e.g., mean, variance, min, max)
*   `"Most common value" <#>`_ (for categorical data)
*   `"Least common value" <#>`_ (for categorical data)

All regridding methods can operate lazily on Dask arrays.

Note that "Most common value" and "Least common value" are designed to regrid categorical data to a coarser resolution. For regridding categorical data to a finer resolution, please use "nearest-neighbor" regridder.

For usage examples, please refer to the `quickstart guide <getting_started.md>`_ and the `example notebooks <notebooks/index.md>`_.

## Installation

For a minimal install:

```console
pip install monet-regrid
```

*Note: monet-regrid is also [available on conda-forge](https://anaconda.org/conda-forge/monet-regrid).*

To improve performance in certain cases:

```console
pip install monet-regrid[accel]
```

which includes optional extras such as:
*   `dask`: parallelization over chunked data
*   `sparse`: for performing conservative regridding using sparse weight matrices
*   `opt-einsum`: optimized einsum routines used in conservative regridding

Benchmarking varies across different hardware specifications, but the inclusion of these extras can often provide significant speedups.

## Usage

The monet-regrid routines are accessed using the "regrid" accessor on an xarray Dataset:

```python
import monet_regrid
import xarray as xr

ds = xr.open_dataset("input_data.nc")
ds_grid = xr.open_dataset("target_grid.nc")

# Using the build_regridder factory API (recommended)
regridder = ds.regrid.build_regridder(ds_grid, method="linear")
regridded_ds = regridder()

# Or directly calling the method (for rectilinear grids)
regridded_ds_direct = ds.regrid.linear(ds_grid)

# For curvilinear grids, build_regridder handles the dispatch automatically:
# curvilinear_regridder = ds.regrid.build_regridder(curvilinear_target_grid, method="nearest")
# regridded_curvilinear_ds = curvilinear_regridder()
```

For examples, see the benchmark notebooks and the demo notebooks.

## Benchmarks

The benchmark notebooks contain comparisons to more standard methods (CDO, ESMF).

To be able to run the notebooks, a conda environment is required (due to ESMF and CDO).
You can install this environment using the `environment.yml` file in this repository.
[Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html) is a lightweight version of the much faster "mamba" conda alternative.

```sh
micromamba create -n environment_name -f environment.yml
```

## Acknowledgements

This package was developed under Netherlands eScience Center grant [NLESC.OEC.2022.017](https://research-software-directory.org/projects/excited).