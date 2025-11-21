# Getting Started

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

``monet-regrid`` allows you to regrid xarray Datasets or DataArrays to a new resolution.
You can install monet-regrid with pip:

```console
pip install monet-regrid
```

To use the package, import ``monet_regrid``. This will register the ``.regrid`` 'accessor' so it can be used.
Next load in the data you want to regrid, and the data with a grid you want to regrid to:

```python
import monet_regrid
import xarray as xr

ds = xr.open_dataset("input_data.nc")
ds_grid = xr.open_dataset("target_grid.nc")

ds = ds.regrid.linear(ds_grid)

# or, for example:
ds = ds.regrid.conservative(ds_grid, latitude_coord="lat")
```

Multiple regridding methods are available:

*   `linear interpolation <#>`_ (``.regrid.linear``)
*   `nearest-neighbor <#>`_ (``.regrid.nearest``)
*   `cubic interpolation <#>`_ (``.regrid.cubic``)
*   `conservative regridding <#>`_ (``.regrid.conservative``)
*   `zonal statistics <#>`_ (``.regrid.stat``) is available to compute statistics such as the maximum value, or variance.

Additionally, there are separate methods available to compute the
`most common value <#>`_ (``.regrid.most_common``) and `least common value <#>`_
(``.regrid.least_common``). This can be used to upscale very fine categorical data to a more course resolution.

## Curvilinear Grids

``monet-regrid`` now supports regridding for curvilinear grids using 3D coordinate transformations. This allows for accurate interpolation on spherical surfaces.

The `build_regridder` factory method automatically detects the grid type and selects the appropriate regridding implementation.

### Using `build_regridder`

The `build_regridder` method is the recommended way to create a regridder, as it handles grid type detection and dispatches to the correct regridder class.

```python
import xarray as xr
import monet_regrid as xrg

# Assume ds_source and ds_target are xarray Datasets with appropriate coordinates

# For rectilinear grids (automatic detection)
regridder_rect = ds_source.regrid.build_regridder(ds_target, method="linear")
regridded_rect = regridder_rect()

# For curvilinear grids (automatic detection)
# Assume ds_source_curvilinear and ds_target_curvilinear are Datasets with 2D lat/lon coordinates
regridder_curvilinear = ds_source_curvilinear.regrid.build_regridder(
    ds_target_curvilinear, method="nearest"
)
regridded_curvilinear = regridder_curvilinear()

# You can also pass additional arguments to the underlying regridder
regridder_conservative = ds_source.regrid.build_regridder(
    ds_target,
    method="conservative",
    skipna=True,
    nan_threshold=0.5
)
regridded_conservative = regridder_conservative()
```

### Curvilinear Grid Examples

Here's a basic example of regridding a curvilinear grid:

```python
import xarray as xr
import numpy as np

# Create a sample curvilinear source grid
source_x, source_y = np.meshgrid(np.arange(5), np.arange(6))
source_lat = 30 + 0.5 * source_x + 0.1 * source_y  # Curvilinear lat
source_lon = -100 + 0.3 * source_x + 0.2 * source_y  # Curvilinear lon

source_grid = xr.Dataset({
    'latitude': (['y', 'x'], source_lat),
    'longitude': (['y', 'x'], source_lon)
})

# Create sample data for the source grid
data_values = np.random.rand(6, 5)  # (y, x)
source_data = xr.DataArray(
    data_values,
    dims=['y', 'x'],
    coords={'y': range(6), 'x': range(5)}
)

# Create a target grid (can be rectilinear or curvilinear)
target_x, target_y = np.meshgrid(np.linspace(0, 4, 3), np.linspace(0, 5, 4))
target_lat = 30 + 0.5 * target_x + 0.1 * target_y
target_lon = -100 + 0.3 * target_x + 0.2 * target_y

target_grid = xr.Dataset({
    'latitude': (['y_target', 'x_target'], target_lat),
    'longitude': (['y_target', 'x_target'], target_lon)
})

# Build the regridder for curvilinear data
regridder = source_data.regrid.build_regridder(target_grid, method="nearest")
regridded_data = regridder()

print(regridded_data)
```

### Backward Compatibility

Existing code that uses the direct method calls (e.g., `ds.regrid.linear(ds_grid)`) will continue to work as before for rectilinear grids. The `build_regridder` method provides a more unified interface that also handles curvilinear grids.

For example, the following code will still work:

```python
# For rectilinear grids, this is equivalent to:
# regridder = ds.regrid.build_regridder(ds_grid, method="linear")
# regridded_ds = regridder()
ds.regrid.linear(ds_grid)