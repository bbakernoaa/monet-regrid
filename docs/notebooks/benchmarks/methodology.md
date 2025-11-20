# Benchmarking Methodology for xarray-regrid

This document outlines the consistent methodology to be used across all benchmark notebooks in the xarray-regrid library.

## General Principles

1. **Timing Measurements**: All performance benchmarks should use the `time.time()` function to measure execution time, with the format `time() - t0` where `t0` is the start time.
2. **Dask Setup**: All notebooks should initialize a Dask client with `client = dask.distributed.Client()` for consistent parallel processing.
3. **Data Loading**: Use ERA5 datasets or synthetic data with consistent dimensions where possible.
4. **Target Grids**: Use the `xarray_regrid.Grid` class to create consistent target grids across benchmarks.
5. **Comparison Metrics**: 
   - Performance: Execution time in seconds
   - Accuracy: Relative error `(a-b)/a` between datasets, root mean squared error (RMSE)

## Standard Benchmark Structure

Each benchmark notebook should follow this structure:

### 1. Imports and Setup
```python
from time import time
import dask.distributed
import xarray_regrid  # Importing this will make Dataset.regrid accessible.
import xarray as xr
from xarray_regrid import Grid
import xesmf as xe

client = dask.distributed.Client()
```

### 2. Data Loading
- Use consistent ERA5 datasets where possible:
  - `data/era5_2m_dewpoint_temperature_2000_monthly.nc` for bilinear/nearest
  - `data/era5_total_precipitation_2020_monthly.nc` for conservative
- For synthetic data, use consistent dimensions and random seeds

### 3. Target Grid Creation
```python
new_grid = Grid(
    north=90,
    east=180,
    south=-90,  # or appropriate southern boundary
    west=-180, # or appropriate western boundary
    resolution_lat=0.25,  # or appropriate resolution
    resolution_lon=0.25,  # or appropriate resolution
)
target_dataset = new_grid.create_regridding_dataset()
```

### 4. Method Testing
For each method being tested:
- Record execution time with `t0 = time()` before and `time() - t0` after
- Ensure computation is triggered with `.compute()` for fair comparison
- Store results for comparison

### 5. Comparison
- Use `benchmark_utils.plot_comparison()` for visual comparison when comparing multiple methods
- Calculate RMSE and relative errors for quantitative comparison
- Use consistent parameters for all methods being compared

## Specific Considerations for Curvilinear Benchmarks

### Curvilinear Grid Creation
When creating curvilinear grids for testing:

```python
# Create 2D coordinate arrays
lon_1d = np.linspace(west, east, nx)
lat_1d = np.linspace(south, north, ny)
lon_2d, lat_2d = np.meshgrid(lon_1d, lat_1d)

# Add realistic distortion for curvilinear grids
lon_2d = lon_2d + distortion_factor * np.sin(np.radians(lat_2d)) * np.cos(np.radians(lon_2d))
lat_2d = lat_2d + distortion_factor * np.cos(np.radians(lat_2d)) * np.sin(np.radians(lon_2d))

# Create dataset with 2D coordinates
curvilinear_ds = xr.Dataset(
    data_vars={
        'variable': (('y', 'x'), data_array)
    },
    coords={
        'lon': (('y', 'x'), lon_2d),
        'lat': (('y', 'x'), lat_2d)
    }
)
```

### Consistent Comparison Metrics
- Compare curvilinear vs rectilinear methods on appropriate grids
- Use the `CurvilinearInterpolator` class for curvilinear tests
- Document when each method type is appropriate

## Performance Measurement Guidelines

1. **Warm-up Runs**: For consistent timing, consider running methods once before timing to account for initialization overhead.
2. **Multiple Runs**: For more accurate timing, run each method multiple times and take the minimum execution time.
3. **Memory Usage**: Note memory usage differences, especially for large grids.
4. **Chunking Strategy**: Document the chunking strategy used, as this can significantly impact performance.

## Accuracy Assessment

1. **Reference Implementation**: When comparing against CDO or xESMF, consider the reference implementation as the baseline.
2. **Error Metrics**: 
   - Relative error: `(method_result - reference) / reference`
   - Absolute error: `abs(method_result - reference)`
   - RMSE: `np.sqrt(np.mean((method_result - reference)**2))`
3. **Edge Effects**: Consider excluding edge regions where regridding may be less accurate.

## Reporting Standards

1. **Timing Results**: Report times to 3 decimal places in seconds
2. **Error Values**: Report errors with appropriate precision based on magnitude
3. **Grid Specifications**: Always document the source and target grid specifications
4. **System Information**: Include information about the system used for benchmarking when relevant