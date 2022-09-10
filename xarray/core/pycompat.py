from __future__ import annotations

from importlib import import_module

import numpy as np
from packaging.version import Version

from .utils import is_duck_array

integer_types = (int, np.integer)


class DuckArrayModule:
    """
    Solely for internal isinstance and version checks.

    Motivated by having to only import pint when required (as pint currently imports xarray)
    https://github.com/pydata/xarray/pull/5561#discussion_r664815718
    """

    def __init__(self, mod):
        try:
            duck_array_module = import_module(mod)
            duck_array_version = Version(duck_array_module.__version__)

            if mod == "dask":
                duck_array_type = (import_module("dask.array").Array,)
            elif mod == "pint":
                duck_array_type = (duck_array_module.Quantity,)
            elif mod == "cupy":
                duck_array_type = (duck_array_module.ndarray,)
            elif mod == "sparse":
                duck_array_type = (duck_array_module.SparseArray,)
            elif mod == "cubed":
                duck_array_type = (duck_array_module.CoreArray,)
            else:
                raise NotImplementedError

        except ImportError as err:  # pragma: no cover
            print(err)
            duck_array_module = None
            duck_array_version = Version("0.0.0")
            duck_array_type = ()

        self.module = duck_array_module
        self.version = duck_array_version
        self.type = duck_array_type
        self.available = duck_array_module is not None


dsk = DuckArrayModule("dask")
dask_version = dsk.version
dask_array_type = dsk.type

sp = DuckArrayModule("sparse")
sparse_array_type = sp.type
sparse_version = sp.version

cub = DuckArrayModule("cubed")
cubed_version = cub.version
cubed_array_type = cub.type

cupy_array_type = DuckArrayModule("cupy").type


def is_dask_collection(x):
    if dsk.available:
        from dask.base import is_dask_collection

        return is_dask_collection(x)
    else:
        return False


def is_duck_dask_array(x):
    return is_duck_array(x) and is_dask_collection(x)


def is_chunked_array(x):
    return is_duck_dask_array(x) or isinstance(x, cubed_array_type)
