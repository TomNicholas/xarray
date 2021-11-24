"""Stub file for mixin classes with arithmetic operators."""
# This file was generated using xarray.util.generate_ops. Do not edit manually.

from typing import NoReturn, TypeVar, Union, overload

import numpy as np

from .dataarray import DataArray
from .dataset import Dataset
from .groupby import DataArrayGroupBy, DatasetGroupBy, GroupBy
from .npcompat import ArrayLike
from .types import (
    DaCompatible,
    DsCompatible,
    GroupByIncompatible,
    ScalarOrArray,
    VarCompatible,
)
from .variable import Variable

try:
    from dask.array import Array as DaskArray
except ImportError:
    DaskArray = np.ndarray

# DatasetOpsMixin etc. are parent classes of Dataset etc.
# Because of https://github.com/pydata/xarray/issues/5755, we redefine these. Generally
# we use the ones in `types`. (We're open to refining this, and potentially integrating
# the `py` & `pyi` files to simplify them.)
T_Dataset = TypeVar("T_Dataset", bound="DatasetOpsMixin")
T_DataArray = TypeVar("T_DataArray", bound="DataArrayOpsMixin")
T_Variable = TypeVar("T_Variable", bound="VariableOpsMixin")

class DatasetOpsMixin:
    __slots__ = ()
    def _binary_op(self, other, f, reflexive=...): ...
    def __add__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __sub__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __mul__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __pow__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __truediv__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __floordiv__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __mod__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __and__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __xor__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __or__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __lt__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __le__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __gt__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __ge__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __eq__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...  # type: ignore[override]
    def __ne__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...  # type: ignore[override]
    def __radd__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rsub__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rmul__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rpow__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rtruediv__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rfloordiv__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rmod__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rand__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __rxor__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def __ror__(self: T_Dataset, other: DsCompatible) -> T_Dataset: ...
    def _inplace_binary_op(self, other, f): ...
    def _unary_op(self, f, *args, **kwargs): ...
    def __neg__(self: T_Dataset) -> T_Dataset: ...
    def __pos__(self: T_Dataset) -> T_Dataset: ...
    def __abs__(self: T_Dataset) -> T_Dataset: ...
    def __invert__(self: T_Dataset) -> T_Dataset: ...
    def round(self: T_Dataset, *args, **kwargs) -> T_Dataset: ...
    def argsort(self: T_Dataset, *args, **kwargs) -> T_Dataset: ...
    def conj(self: T_Dataset, *args, **kwargs) -> T_Dataset: ...
    def conjugate(self: T_Dataset, *args, **kwargs) -> T_Dataset: ...

class DataArrayOpsMixin:
    __slots__ = ()
    def _binary_op(self, other, f, reflexive=...): ...
    @overload
    def __add__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __add__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __add__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __sub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __sub__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __sub__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __mul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mul__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __mul__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __pow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __pow__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __pow__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __truediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __truediv__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __truediv__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __floordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __floordiv__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __floordiv__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __mod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mod__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __mod__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __and__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __and__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __and__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __xor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __xor__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __xor__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __or__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __or__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __or__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __lt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __lt__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __lt__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __le__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __le__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __le__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __gt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __gt__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __gt__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __ge__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ge__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __ge__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload  # type: ignore[override]
    def __eq__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __eq__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __eq__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload  # type: ignore[override]
    def __ne__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ne__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __ne__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __radd__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __radd__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __radd__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rsub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rsub__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rsub__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rmul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmul__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rmul__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rpow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rpow__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rpow__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rtruediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rtruediv__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rtruediv__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rfloordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rfloordiv__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rfloordiv__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rmod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmod__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rmod__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rand__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rand__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rand__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __rxor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rxor__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rxor__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    @overload
    def __ror__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ror__(self, other: "DatasetGroupBy") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __ror__(self: T_DataArray, other: DaCompatible) -> T_DataArray: ...
    def _inplace_binary_op(self, other, f): ...
    def _unary_op(self, f, *args, **kwargs): ...
    def __neg__(self: T_DataArray) -> T_DataArray: ...
    def __pos__(self: T_DataArray) -> T_DataArray: ...
    def __abs__(self: T_DataArray) -> T_DataArray: ...
    def __invert__(self: T_DataArray) -> T_DataArray: ...
    def round(self: T_DataArray, *args, **kwargs) -> T_DataArray: ...
    def argsort(self: T_DataArray, *args, **kwargs) -> T_DataArray: ...
    def conj(self: T_DataArray, *args, **kwargs) -> T_DataArray: ...
    def conjugate(self: T_DataArray, *args, **kwargs) -> T_DataArray: ...

class VariableOpsMixin:
    __slots__ = ()
    def _binary_op(self, other, f, reflexive=...): ...
    @overload
    def __add__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __add__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __add__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __sub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __sub__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __sub__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __mul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mul__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __mul__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __pow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __pow__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __pow__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __truediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __truediv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __truediv__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __floordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __floordiv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __floordiv__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __mod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mod__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __mod__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __and__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __and__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __and__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __xor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __xor__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __xor__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __or__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __or__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __or__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __lt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __lt__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __lt__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __le__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __le__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __le__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __gt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __gt__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __gt__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __ge__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ge__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __ge__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload  # type: ignore[override]
    def __eq__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __eq__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __eq__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload  # type: ignore[override]
    def __ne__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ne__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __ne__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __radd__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __radd__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __radd__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rsub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rsub__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rsub__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rmul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmul__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rmul__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rpow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rpow__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rpow__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rtruediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rtruediv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rtruediv__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rfloordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rfloordiv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rfloordiv__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rmod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmod__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rmod__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rand__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rand__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rand__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __rxor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rxor__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rxor__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    @overload
    def __ror__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ror__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __ror__(self: T_Variable, other: VarCompatible) -> T_Variable: ...
    def _inplace_binary_op(self, other, f): ...
    def _unary_op(self, f, *args, **kwargs): ...
    def __neg__(self: T_Variable) -> T_Variable: ...
    def __pos__(self: T_Variable) -> T_Variable: ...
    def __abs__(self: T_Variable) -> T_Variable: ...
    def __invert__(self: T_Variable) -> T_Variable: ...
    def round(self: T_Variable, *args, **kwargs) -> T_Variable: ...
    def argsort(self: T_Variable, *args, **kwargs) -> T_Variable: ...
    def conj(self: T_Variable, *args, **kwargs) -> T_Variable: ...
    def conjugate(self: T_Variable, *args, **kwargs) -> T_Variable: ...

class DatasetGroupByOpsMixin:
    __slots__ = ()
    def _binary_op(self, other, f, reflexive=...): ...
    @overload
    def __add__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __add__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __add__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __sub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __sub__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __sub__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __mul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mul__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __mul__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __pow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __pow__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __pow__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __truediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __truediv__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __truediv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __floordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __floordiv__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __floordiv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __mod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mod__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __mod__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __and__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __and__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __and__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __xor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __xor__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __xor__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __or__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __or__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __or__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __lt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __lt__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __lt__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __le__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __le__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __le__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __gt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __gt__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __gt__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __ge__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ge__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __ge__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload  # type: ignore[override]
    def __eq__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __eq__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __eq__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload  # type: ignore[override]
    def __ne__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ne__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __ne__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __radd__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __radd__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __radd__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rsub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rsub__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rsub__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rmul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmul__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rmul__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rpow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rpow__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rpow__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rtruediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rtruediv__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rtruediv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rfloordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rfloordiv__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rfloordiv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rmod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmod__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rmod__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rand__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rand__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rand__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rxor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rxor__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __rxor__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __ror__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ror__(self, other: "DataArray") -> "Dataset": ...  # type: ignore[misc]
    @overload
    def __ror__(self, other: GroupByIncompatible) -> NoReturn: ...

class DataArrayGroupByOpsMixin:
    __slots__ = ()
    def _binary_op(self, other, f, reflexive=...): ...
    @overload
    def __add__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __add__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __add__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __sub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __sub__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __sub__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __mul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mul__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __mul__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __pow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __pow__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __pow__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __truediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __truediv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __truediv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __floordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __floordiv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __floordiv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __mod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __mod__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __mod__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __and__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __and__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __and__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __xor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __xor__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __xor__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __or__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __or__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __or__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __lt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __lt__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __lt__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __le__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __le__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __le__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __gt__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __gt__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __gt__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __ge__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ge__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __ge__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload  # type: ignore[override]
    def __eq__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __eq__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __eq__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload  # type: ignore[override]
    def __ne__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ne__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __ne__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __radd__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __radd__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __radd__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rsub__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rsub__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rsub__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rmul__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmul__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rmul__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rpow__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rpow__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rpow__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rtruediv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rtruediv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rtruediv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rfloordiv__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rfloordiv__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rfloordiv__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rmod__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rmod__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rmod__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rand__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rand__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rand__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __rxor__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __rxor__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __rxor__(self, other: GroupByIncompatible) -> NoReturn: ...
    @overload
    def __ror__(self, other: T_Dataset) -> T_Dataset: ...
    @overload
    def __ror__(self, other: T_DataArray) -> T_DataArray: ...
    @overload
    def __ror__(self, other: GroupByIncompatible) -> NoReturn: ...
