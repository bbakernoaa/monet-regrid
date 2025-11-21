import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

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


def plot_comparison(data_regrid, data_esmf, data_cdo, vmin, vmax, varname):
    def relative_error(a, b):
        return (a - b) / a

    esmf_v_regrid = relative_error(data_esmf, data_regrid).isel(time=0)[varname]
    cdo_v_regrid = relative_error(data_cdo, data_regrid).isel(time=0)[varname]
    esmf_v_cdo = relative_error(data_esmf, data_cdo).isel(time=0)[varname]

    # Set up figure and image
    fig = plt.figure(1, (11, 5), dpi=250)
    axes = ImageGrid(
        fig,
        rect=111,  # as in plt.subplot(111)
        nrows_ncols=(1, 3),
        axes_pad=0.15,
        share_all=True,
        cbar_location="right",
        cbar_mode="single",
        cbar_size="7%",
        cbar_pad=0.15,
    )

    kwargs = {"vmin": vmin, "vmax": vmax, "add_colorbar": False, "cmap": "bwr"}
    im = esmf_v_regrid.plot(ax=axes[0], **kwargs)
    cdo_v_regrid.plot(ax=axes[1], **kwargs)
    esmf_v_cdo.plot(ax=axes[2], **kwargs)

    for ax in axes:
        ax.set_xlabel("longitude")

    ax.cax.colorbar(im)
    ax.cax.toggle_label(True)

    for ax in axes[1:]:
        ax.set_ylabel("")
    axes[0].set_ylabel("latitude")

    axes[0].set_title("xESMF vs. monet-regrid")
    axes[1].set_title("CDO vs. monet-regrid")
    axes[2].set_title("xESMF vs. CDO")

    plt.show()
