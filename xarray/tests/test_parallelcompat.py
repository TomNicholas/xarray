from __future__ import annotations

from typing import Any, Optional, Union

import numpy as np
import pytest

from xarray.core.daskmanager import DaskManager
from xarray.core.parallelcompat import (
    ChunkManagerEntrypoint,
    T_Chunks,
    get_chunked_array_type,
    guess_chunkmanager,
    list_chunkmanagers,
)
from xarray.tests import has_dask, requires_dask


class DummyChunkedArray(np.ndarray):
    """
    Mock-up of a chunked array class.

    Adds a (non-functional) .chunks attribute by following this example in the numpy docs
    https://numpy.org/doc/stable/user/basics.subclassing.html#simple-example-adding-an-extra-attribute-to-ndarray
    """

    chunks: Optional[T_Chunks]

    def __new__(
        cls,
        shape,
        dtype=float,
        buffer=None,
        offset=0,
        strides=None,
        order=None,
        chunks=None,
    ):
        obj = super().__new__(cls, shape, dtype, buffer, offset, strides, order)
        obj.chunks = chunks
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.chunks = getattr(obj, "chunks", None)

    def rechunk(self, chunks, **kwargs):
        copied = self.copy()
        copied.chunks = chunks
        return copied


class DummyChunkManager(ChunkManagerEntrypoint):
    """Mock-up of ChunkManager class for DummyChunkedArray"""

    def __init__(self):
        self.array_cls = DummyChunkedArray

    def is_chunked_array(self, data: Any) -> bool:
        return isinstance(data, DummyChunkedArray)

    def chunks(self, data: DummyChunkedArray) -> T_Chunks:
        return data.chunks

    def normalize_chunks(
        self,
        chunks: Union[tuple, int, dict, str],
        shape: Union[tuple[int], None] = None,
        limit: Union[int, None] = None,
        dtype: Union[np.dtype, None] = None,
        previous_chunks: Union[tuple[tuple[int, ...], ...], None] = None,
    ) -> tuple[tuple[int, ...], ...]:
        from dask.array.core import normalize_chunks

        return normalize_chunks(chunks, shape, limit, dtype, previous_chunks)

    def from_array(
        self, data: np.ndarray, chunks: T_Chunks, **kwargs
    ) -> DummyChunkedArray:
        from dask import array as da

        return da.from_array(data, chunks, **kwargs)

    def rechunk(self, data: DummyChunkedArray, chunks, **kwargs) -> DummyChunkedArray:
        return data.rechunk(chunks, **kwargs)

    def compute(self, *data: DummyChunkedArray, **kwargs) -> np.ndarray:
        from dask.array import compute

        return compute(*data, **kwargs)

    def apply_gufunc(
        self,
        func,
        signature,
        *args,
        axes=None,
        axis=None,
        keepdims=False,
        output_dtypes=None,
        output_sizes=None,
        vectorize=None,
        allow_rechunk=False,
        meta=None,
        **kwargs,
    ):
        from dask.array.gufunc import apply_gufunc

        return apply_gufunc(
            func,
            signature,
            *args,
            axes=axes,
            axis=axis,
            keepdims=keepdims,
            output_dtypes=output_dtypes,
            output_sizes=output_sizes,
            vectorize=vectorize,
            allow_rechunk=allow_rechunk,
            meta=meta,
            **kwargs,
        )


@pytest.fixture
def register_dummy_chunkmanager(monkeypatch):
    """
    Mocks the registering of an additional ChunkManagerEntrypoint.

    This preserves the presence of the existing DaskManager, so a test that relies on this and DaskManager both being
    returned from list_chunkmanagers() at once would still work.

    The monkeypatching changes the behavior of list_chunkmanagers when called inside xarray.core.parallelcompat,
    but not when called from this tests file.
    """
    # Should include DaskManager iff dask is available to be imported
    preregistered_chunkmanagers = list_chunkmanagers()

    monkeypatch.setattr(
        "xarray.core.parallelcompat.list_chunkmanagers",
        lambda: {"dummy": DummyChunkManager()} | preregistered_chunkmanagers,
    )
    yield


class TestGetChunkManager:
    def test_get_chunkmanger(self, register_dummy_chunkmanager):
        chunkmanager = guess_chunkmanager("dummy")
        assert isinstance(chunkmanager, DummyChunkManager)

    def test_fail_on_nonexistent_chunkmanager(self):
        with pytest.raises(ValueError, match="unrecognized chunk manager foo"):
            guess_chunkmanager("foo")

    @requires_dask
    def test_get_dask_if_installed(self):
        chunkmanager = guess_chunkmanager(None)
        assert isinstance(chunkmanager, DaskManager)

    @pytest.mark.skipif(has_dask, reason="requires dask not to be installed")
    def test_dont_get_dask_if_not_installed(self):
        with pytest.raises(ValueError, match="unrecognized chunk manager dask"):
            guess_chunkmanager("dask")

    @requires_dask
    def test_choose_dask_over_other_chunkmanagers(self, register_dummy_chunkmanager):
        chunk_manager = guess_chunkmanager(None)
        assert isinstance(chunk_manager, DaskManager)


class TestGetChunkedArrayType:
    def test_detect_chunked_arrays(self, register_dummy_chunkmanager):
        dummy_arr = DummyChunkedArray([1, 2, 3])

        chunk_manager = get_chunked_array_type(dummy_arr)
        assert isinstance(chunk_manager, DummyChunkManager)

    def test_ignore_inmemory_arrays(self, register_dummy_chunkmanager):
        dummy_arr = DummyChunkedArray([1, 2, 3])

        chunk_manager = get_chunked_array_type(*[dummy_arr, 1.0, np.array([5, 6])])
        assert isinstance(chunk_manager, DummyChunkManager)

        with pytest.raises(TypeError, match="Expected a chunked array"):
            get_chunked_array_type(5.0)

    def test_raise_if_no_arrays_chunked(self, register_dummy_chunkmanager):
        with pytest.raises(TypeError, match="Expected a chunked array "):
            get_chunked_array_type(*[1.0, np.array([5, 6])])

    def test_raise_if_no_matching_chunkmanagers(self):
        dummy_arr = DummyChunkedArray([1, 2, 3])

        with pytest.raises(
            TypeError, match="Could not find a Chunk Manager which recognises"
        ):
            get_chunked_array_type(dummy_arr)

    @requires_dask
    def test_detect_dask_if_installed(self):
        import dask.array as da

        dask_arr = da.from_array([1, 2, 3], chunks=(1,))

        chunk_manager = get_chunked_array_type(dask_arr)
        assert isinstance(chunk_manager, DaskManager)

    @requires_dask
    def test_raise_on_mixed_array_types(self, register_dummy_chunkmanager):
        import dask.array as da

        dummy_arr = DummyChunkedArray([1, 2, 3])
        dask_arr = da.from_array([1, 2, 3], chunks=(1,))

        with pytest.raises(TypeError, match="received multiple types"):
            get_chunked_array_type(*[dask_arr, dummy_arr])
