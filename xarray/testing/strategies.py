from typing import Any, Callable, List, Mapping, Optional, Sequence, Set, Tuple, Union
import string

import hypothesis.extra.numpy as npst
import hypothesis.strategies as st
import numpy as np
from hypothesis import assume

import xarray as xr
from xarray.core.utils import is_dict_like

from . import utils

# required to exclude weirder dtypes e.g. unicode, byte_string, array, or nested dtypes.
valid_dtypes: st.SearchStrategy[np.dtype] = (
    npst.integer_dtypes()
    | npst.unsigned_integer_dtypes()
    | npst.floating_dtypes()
    | npst.complex_number_dtypes()
)


def elements(dtype) -> st.SearchStrategy[Any]:
    max_value = 100
    min_value = 0 if dtype.kind == "u" else -max_value

    return npst.from_dtype(
        dtype, allow_infinity=False, min_value=min_value, max_value=max_value
    )


def numpy_array(shape, dtypes=None) -> st.SearchStrategy[np.ndarray]:
    if dtypes is None:
        dtypes = all_dtypes

    return dtypes.flatmap(
        lambda dtype: npst.arrays(dtype=dtype, shape=shape, elements=elements(dtype))
    )


def dimension_sizes(
    min_dims, max_dims, min_size, max_size
) -> st.SearchStrategy[List[Tuple[str, int]]]:
    sizes = st.lists(
        elements=st.tuples(st.text(min_size=1), st.integers(min_size, max_size)),
        min_size=min_dims,
        max_size=max_dims,
        unique_by=lambda x: x[0],
    )
    return sizes


@st.composite
def np_arrays(
    draw: st.DrawFn,
    shape: Union[Tuple[int], st.SearchStrategy[Tuple[int]]] = None,
    dtype: Union[np.dtype, st.SearchStrategy[np.dtype]] = None,
) -> st.SearchStrategy[np.ndarray]:
    """
    Generates arbitrary numpy arrays with xarray-compatible dtypes.

    Parameters
    ----------
    shape
    dtype
        Default is to use any of the valid_dtypes defined for xarray.
    """
    if shape is None:
        shape = draw(npst.array_shapes())
    elif isinstance(shape, st.SearchStrategy):
        shape = draw(shape)

    if dtype is None:
        dtype = draw(valid_dtypes)
    elif isinstance(dtype, st.SearchStrategy):
        dtype = draw(dtype)

    return draw(npst.arrays(dtype=dtype, shape=shape, elements=elements(dtype)))


def dimension_names(
    min_ndims: int = 0,
    max_ndims: int = 3,
) -> st.SearchStrategy[List[str]]:
    """
    Generates arbitrary lists of valid dimension names.
    """

    return st.lists(
        elements=st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=5),
        min_size=min_ndims,
        max_size=max_ndims,
        unique=True,
    )


# Is there a way to do this in general?
# Could make a Protocol...
T_Array = Any


@st.composite
def variables(
    draw: st.DrawFn,
    dims: Union[Sequence[str], st.SearchStrategy[str]] = None,
    data: Union[T_Array, st.SearchStrategy[T_Array], None] = None,
    attrs=None,
    convert: Callable[[np.ndarray], T_Array] = lambda a: a,
) -> st.SearchStrategy[xr.Variable]:
    """
    Generates arbitrary xarray.Variable objects.

    Follows the signature of the xarray.Variable constructor, but you can also pass alternative strategies to generate
    either numpy-like array data or dimension names. Passing both at once is forbidden.

    Passing nothing will generate a completely arbitrary Variable (backed by a numpy array).

    Parameters
    ----------
    data: array-like, strategy which generates array-likes, or None
        Default is to generate numpy data of arbitrary shape, values and dtype.
    dims: Sequence of str, strategy which generates sequence of str, or None
        Default is to generate arbitrary dimension names for each axis in data.
    attrs: None
    convert: Callable
        Function which accepts one numpy array and returns one numpy-like array.
        Default is a no-op.
    """

    if isinstance(data, st.SearchStrategy) and isinstance(dims, st.SearchStrategy):
        # TODO could we relax this by adding a constraint?
        raise TypeError(
            "Passing strategies for both dims and data could generate inconsistent contents for Variable"
        )

    if data is not None and isinstance(data, st.SearchStrategy):
        data = draw(data)
    if dims is not None and isinstance(dims, st.SearchStrategy):
        dims = draw(dims)

    print(dims)
    print(data)

    if data is not None and not dims:
        # no dims -> generate dims to match data
        dims = draw(dimension_names(min_ndims=data.ndim, max_ndims=data.ndim))

    elif dims is not None and data is None:
        # no data -> generate data to match dims
        valid_shapes = npst.array_shapes(min_dims=len(dims), max_dims=len(dims))
        data = draw(np_arrays(shape=draw(valid_shapes)))

    elif data is not None and dims is not None:
        # both data and dims provided -> check both are compatible
        # TODO is this pointless because the xr.Variable constructor will check this anyway?
        if len(dims) != data.ndim:
            raise ValueError(
                "Explicitly provided data must match explicitly provided dims, "
                f"but len(dims) = {len(dims)} vs len(data.ndim) = {data.ndim}"
            )

    else:
        # nothing provided, so generate everything, but consistently
        data = np_arrays()
        # TODO this should be possible with flatmap
        print(draw(data).ndim)
        dims = data.flatmap(
            lambda arr: dimension_names(min_ndims=arr.ndim, max_ndims=arr.ndim)
        )
        # dims = draw(dimension_names())
        # assume(len(dims) == data.ndim)

    # duckarray = convert(data)

    # print(data)
    # print(dims)
    return xr.Variable(dims=dims, data=data, attrs=attrs)


@st.composite
def dataarrays(
    draw: st.DrawFn,
    create_data: Callable,
    *,
    min_dims=1,
    max_dims=3,
    min_size=1,
    max_size=3,
    dtypes=None,
) -> st.SearchStrategy[xr.DataArray]:

    name = draw(st.none() | st.text(min_size=1))
    if dtypes is None:
        dtypes = all_dtypes

    sizes = st.lists(
        elements=st.tuples(st.text(min_size=1), st.integers(min_size, max_size)),
        min_size=min_dims,
        max_size=max_dims,
        unique_by=lambda x: x[0],
    )
    drawn_sizes = draw(sizes)
    dims, shape = zip(*drawn_sizes)

    data = draw(create_data(shape, dtypes))

    return xr.DataArray(
        data=data,
        name=name,
        dims=dims,
    )


@st.composite
def datasets(
    draw: st.DrawFn,
    create_data: Callable,
    *,
    min_dims=1,
    max_dims=3,
    min_size=1,
    max_size=3,
    min_vars=1,
    max_vars=3,
) -> st.SearchStrategy[xr.Dataset]:

    dtypes = st.just(draw(all_dtypes))
    names = st.text(min_size=1)
    sizes = dimension_sizes(
        min_size=min_size, max_size=max_size, min_dims=min_dims, max_dims=max_dims
    )

    data_vars = sizes.flatmap(
        lambda s: st.dictionaries(
            keys=names.filter(lambda n: n not in dict(s)),
            values=variables(create_data, sizes=s, dtypes=dtypes),
            min_size=min_vars,
            max_size=max_vars,
        )
    )

    return xr.Dataset(data_vars=draw(data_vars))


def valid_axis(ndim) -> st.SearchStrategy[Union[None, int]]:
    if ndim == 0:
        return st.none() | st.just(0)
    return st.none() | st.integers(-ndim, ndim - 1)


def valid_axes(ndim) -> st.SearchStrategy[Union[None, int, Tuple[int, ...]]]:
    return valid_axis(ndim) | npst.valid_tuple_axes(ndim, min_size=1)


def valid_dim(dims) -> st.SearchStrategy[str]:
    if not isinstance(dims, list):
        dims = [dims]

    ndim = len(dims)
    axis = valid_axis(ndim)
    return axis.map(lambda axes: utils.valid_dims_from_axes(dims, axes))


def valid_dims(dims) -> st.SearchStrategy[xr.DataArray]:
    if is_dict_like(dims):
        dims = list(dims.keys())
    elif isinstance(dims, tuple):
        dims = list(dims)
    elif not isinstance(dims, list):
        dims = [dims]

    ndim = len(dims)
    axes = valid_axes(ndim)
    return axes.map(lambda axes: utils.valid_dims_from_axes(dims, axes))


@st.composite
def block_lengths(
    draw: st.DrawFn,
    ax_length: int,
    min_chunk_length: int = 1,
    max_chunk_length: Optional[int] = None,
) -> st.SearchStrategy[Tuple[int, ...]]:
    """Generate different chunking patterns along one dimension of an array."""

    chunks = []
    remaining_length = ax_length
    while remaining_length > 0:
        _max_chunk_length = (
            min(remaining_length, max_chunk_length)
            if max_chunk_length
            else remaining_length
        )

        if min_chunk_length > _max_chunk_length:
            # if we are at the end of the array we have no choice but to use a smaller chunk
            chunk = remaining_length
        else:
            chunk = draw(
                st.integers(min_value=min_chunk_length, max_value=_max_chunk_length)
            )

        chunks.append(chunk)
        remaining_length = remaining_length - chunk

    return tuple(chunks)


# TODO we could remove this once dask/9374 is merged upstream
@st.composite
def chunks(
    draw: st.DrawFn,
    shape: Tuple[int, ...],
    axes: Optional[Union[int, Tuple[int, ...]]] = None,
    min_chunk_length: int = 1,
    max_chunk_length: Optional[int] = None,
) -> st.SearchStrategy[Tuple[Tuple[int, ...], ...]]:
    """
    Generates different chunking patterns for an N-D array with a given shape.

    Returns chunking structure as a tuple of tuples of ints, with each inner tuple containing
    the block lengths along one dimension of the array.

    You can limit chunking to specific axes using the `axes` kwarg, and specify minimum and
    maximum block lengths.

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    shape : tuple of ints
        Shape of the array for which you want to generate a chunking pattern.
    axes : None or int or tuple of ints, optional
        ...
    min_chunk_length : int, default is 1
        Minimum chunk length to use along all axes.
    max_chunk_length: int, optional
        Maximum chunk length to use along all axes.
        Default is that the chunk can be as long as the length of the array along that axis.

    Examples
    --------
    Chunking along all axes by default

    >>> chunks(shape=(2, 3)).example()
    ((1, 1), (1, 2))

    Chunking only along the second axis

    >>> chunks(shape=(2, 3), axis=1).example()
    ((2,), (1, 1, 1))

    Minimum size chunks of length 2 along all axes

    >>> chunks(shape=(2, 3), min_chunk_length=2).example()
    ((2,), (2, 1))

    Smallest possible chunks along all axes

    >>> chunks(shape=(2, 3), max_chunk_length=1).example()
    ((1, 1), (1, 1, 1))

    Maximum size chunks along all axes

    >>> chunks(shape=(2, 3), axes=()).example()
    ((2,), (3,))

    See Also
    --------
    testing.strategies.chunks
    DataArray.chunk
    DataArray.chunks
    """

    if min_chunk_length < 1 or not isinstance(min_chunk_length, int):
        raise ValueError("min_chunk_length must be an integer >= 1")

    if max_chunk_length:
        if max_chunk_length < 1 or not isinstance(min_chunk_length, int):
            raise ValueError("max_chunk_length must be an integer >= 1")

    if axes is None:
        axes = tuple(range(len(shape)))
    elif isinstance(axes, int):
        axes = (axes,)

    chunks = []
    for axis, ax_length in enumerate(shape):

        _max_chunk_length = (
            min(max_chunk_length, ax_length) if max_chunk_length else ax_length
        )

        if axes is not None and axis in axes:
            block_lengths_along_ax = draw(
                block_lengths(
                    ax_length,
                    min_chunk_length=min_chunk_length,
                    max_chunk_length=_max_chunk_length,
                )
            )
        else:
            # don't chunk along this dimension
            block_lengths_along_ax = (ax_length,)

        chunks.append(block_lengths_along_ax)

    return tuple(chunks)


@st.composite
def chunksizes(
    draw: st.DrawFn,
    sizes: Mapping[str, int],
    dims: Set[str] = None,
    min_chunk_length: int = 1,
    max_chunk_length: int = None,
) -> st.SearchStrategy[Mapping[str, Tuple[int, ...]]]:
    """
    Generate different chunking patterns for an xarray object with given sizes.

    Returns chunking structure as a mapping of dimension names to tuples of ints,
    with each tuple containing the block lengths along one dimension of the object.

    You can limit chunking to specific dimensions given by the `dim` kwarg.

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    sizes : mapping of dimension names to ints
        Size of the object for which you want to generate a chunking pattern.
    dims : set of str, optional
        Dimensions to chunk along. Default is to chunk along all dimensions.
    min_chunk_length : int, default is 1
        Minimum chunk length to use along all dimensions.
    max_chunk_length: int, optional
        Maximum chunk length to use along all dimensions.
        Default is that the chunk can be as long as the length of the array along that dimension.

    See Also
    --------
    testing.strategies.chunks
    DataArray.chunk
    DataArray.chunksizes
    DataArray.sizes
    """
    shape = tuple(sizes.values())
    axes = tuple(list(sizes.keys()).index(d) for d in dims) if dims else None
    _chunks = draw(
        chunks(
            shape=shape,
            axes=axes,
            min_chunk_length=min_chunk_length,
            max_chunk_length=max_chunk_length,
        )
    )

    return {d: c for d, c in zip(list(sizes.keys()), _chunks)}
