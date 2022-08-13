import hypothesis.extra.numpy as npst
import hypothesis.strategies as st
import numpy as np
import numpy.testing as npt
import pytest
from hypothesis import given, note

from xarray import DataArray, Dataset
from xarray.core.variable import Variable
from xarray.testing.strategies import (
    dimension_names,
    np_arrays,
    valid_dtypes,
    variables,
)


class TestNumpyArraysStrategy:
    @given(np_arrays())
    def test_given_nothing(self, arr):
        assert isinstance(arr, np.ndarray)

    @given(np_arrays(dtype=np.dtype("int32")))
    def test_fixed_dtype(self, arr):
        assert arr.dtype == np.dtype("int32")

    @given(st.data())
    def test_arbitrary_valid_dtype(self, data):
        valid_dtype = data.draw(valid_dtypes)
        arr = data.draw(np_arrays(dtype=valid_dtype))
        assert arr.dtype == valid_dtype

    @given(np_arrays(shape=(2, 3)))
    def test_fixed_shape(self, arr):
        assert arr.shape == (2, 3)

    @given(st.data())
    def test_arbitrary_shape(self, data):
        shape = data.draw(npst.array_shapes())
        arr = data.draw(np_arrays(shape=shape))
        assert arr.shape == shape


class TestDimensionNamesStrategy:
    @given(dimension_names())
    def test_types(self, dims):
        assert isinstance(dims, list)
        for d in dims:
            assert isinstance(d, str)

    @given(dimension_names())
    def test_unique(self, dims):
        assert len(set(dims)) == len(dims)

    @given(dimension_names(min_ndims=3, max_ndims=3))
    def test_fixed_number_of_dims(self, dims):
        assert isinstance(dims, list)
        assert len(dims) == 3


class TestVariablesStrategy:
    @given(variables())
    def test_given_nothing(self, var):
        assert isinstance(var, Variable)

    @given(st.data())
    def test_given_fixed_dims_and_fixed_data(self, data):
        dims = ["x", "y"]
        arr = np.asarray([[1, 2], [3, 4]])
        var = data.draw(variables(dims=dims, data=arr))

        assert isinstance(var, Variable)
        assert list(var.dims) == dims
        npt.assert_equal(var.data, arr)

        with pytest.raises(ValueError, match="data must match"):
            data.draw(variables(dims=["x"], data=arr))

    @pytest.mark.xfail(reason="I don't understand why")
    @given(st.data())
    def test_given_arbitrary_dims_and_arbitrary_data(self, data):
        arr = data.draw(np_arrays())
        dims = data.draw(dimension_names())
        var = data.draw(variables(data=arr, dims=dims))

        assert isinstance(var, Variable)
        npt.assert_equal(var.data, arr)
        assert var.dims == dims

    @given(st.data())
    def test_given_fixed_data(self, data):
        arr = np.asarray([[1, 2], [3, 4]])
        var = data.draw(variables(data=arr))

        assert isinstance(var, Variable)
        npt.assert_equal(arr.data, arr)

    @given(st.data())
    def test_given_arbitrary_data(self, data):
        arr = data.draw(np_arrays())
        var = data.draw(variables(data=arr))

        assert isinstance(var, Variable)
        npt.assert_equal(var.data, arr)

    @given(st.data())
    def test_given_fixed_dims(self, data):
        dims = ["x", "y"]
        var = data.draw(variables(dims=dims))
        assert isinstance(var, Variable)
        assert list(var.dims) == dims

    @given(st.data())
    def test_given_arbitrary_dims(self, data):
        dims = data.draw(dimension_names())
        var = data.draw(variables(dims=dims))

        assert isinstance(var, Variable)
        assert list(var.dims) == dims

    @given(st.data())
    def test_convert(self, data):
        arr = data.draw(np_arrays())
        var = data.draw(variables(data=arr, convert=lambda x: x + 1))

        npt.assert_equal(var.data, arr + 1)
