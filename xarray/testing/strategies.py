from collections.abc import Hashable, Mapping, Sequence
from typing import Any, Protocol, Union

import hypothesis.extra.numpy as npst
import hypothesis.strategies as st
import numpy as np

import xarray as xr
from xarray.core.types import T_DuckArray

__all__ = [
    "supported_dtypes",
    "names",
    "dimension_names",
    "dimension_sizes",
    "attrs",
    "variables",
    "unique_subset_of",
]


class ArrayStrategyFn(Protocol):
    def __call__(
        self,
        *,
        shape: Union[tuple[int, ...], None] = None,
        dtype: Union[np.dtype, None] = None,
        **kwargs,
    ) -> st.SearchStrategy[T_DuckArray]:
        ...


#
def supported_dtypes() -> st.SearchStrategy[np.dtype]:
    """
    Generates only those numpy dtypes which xarray can handle.

    Requires the hypothesis package to be installed.

    Not just using hypothesis.extra.numpy.scalar_dtypes is required to exclude weirder dtypes
    e.g. unicode, byte_string, array, or nested dtypes.
    Also required to dodge bugs with pandas non-nanosecond datetime overflows.
    """
    # TODO should this be exposed publicly?
    # We should decide what the set of numpy dtypes that xarray officially supports is.
    return (
        npst.integer_dtypes()
        | npst.unsigned_integer_dtypes()
        | npst.floating_dtypes()
        | npst.complex_number_dtypes()
    )


def smallish_arrays(
    shape: Union[
        tuple[int, ...], st.SearchStrategy[tuple[int, ...]]
    ] = npst.array_shapes(max_side=4),
    dtype: Union[np.dtype, st.SearchStrategy[np.dtype]] = supported_dtypes(),
    *,
    elements=None,
    fill=None,
    unique=False,
) -> st.SearchStrategy[np.ndarray]:
    """
    Generates arbitrary array API-compliant numpy arrays.

    By default generates arrays with no more than 4 elements per axis for performance, using supported_dtypes.

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    shape
    dtype
        Default is to use any of the scalar dtypes defined in the array API standard.
    elements
    fill
    unique
    """
    # TODO here we may also wish to generalize/restrict the dtypes produced by xarray's default test strategies
    return npst.arrays(
        dtype=dtype, shape=shape, elements=elements, fill=fill, unique=unique
    )


# TODO Generalize to all valid unicode characters once formatting bugs in xarray's reprs are fixed + docs can handle it.
_readable_characters = st.characters(
    categories=["L", "N"], max_codepoint=0x017F
)  # only use characters within the "Latin Extended-A" subset of unicode


def names() -> st.SearchStrategy[str]:
    """
    Generates arbitrary string names for dimensions / variables.

    Requires the hypothesis package to be installed.
    """
    return st.text(
        _readable_characters,
        min_size=1,
        max_size=5,
    )


def dimension_names(
    *,
    min_dims: int = 0,
    max_dims: int = 3,
) -> st.SearchStrategy[list[Hashable]]:
    """
    Generates an arbitrary list of valid dimension names.

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    min_dims
        Minimum number of dimensions in generated list.
    max_dims
        Maximum number of dimensions in generated list.
    """

    return st.lists(
        elements=names(),
        min_size=min_dims,
        max_size=max_dims,
        unique=True,
    )


def dimension_sizes(
    *,
    dim_names: st.SearchStrategy[Hashable] = names(),
    min_dims: int = 0,
    max_dims: int = 3,
    min_side: int = 1,
    max_side: Union[int, None] = None,
) -> st.SearchStrategy[Mapping[Hashable, int]]:
    """
    Generates an arbitrary mapping from dimension names to lengths.

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    dim_names: strategy generating strings, optional
        Strategy for generating dimension names.
        Defaults to the `names` strategy.
    min_dims: int, optional
        Minimum number of dimensions in generated list.
        Default is 1.
    max_dims: int, optional
        Maximum number of dimensions in generated list.
        Default is 3.
    min_side: int, optional
        Minimum size of a dimension.
        Default is 1.
    max_side: int, optional
        Minimum size of a dimension.
        Default is `min_length` + 5.
    """

    if max_side is None:
        max_side = min_side + 3

    return st.dictionaries(
        keys=dim_names,
        values=st.integers(min_value=min_side, max_value=max_side),
        min_size=min_dims,
        max_size=max_dims,
    )


_readable_strings = st.text(
    _readable_characters,
    max_size=5,
)
_attr_keys = _readable_strings
_small_arrays = npst.arrays(
    shape=npst.array_shapes(
        max_side=2,
        max_dims=2,
    ),
    dtype=npst.scalar_dtypes(),
)
_attr_values = st.none() | st.booleans() | _readable_strings | _small_arrays


def attrs() -> st.SearchStrategy[Mapping[Hashable, Any]]:
    """
    Generates arbitrary valid attributes dictionaries for xarray objects.

    The generated dictionaries can potentially be recursive.

    Requires the hypothesis package to be installed.
    """
    return st.recursive(
        st.dictionaries(_attr_keys, _attr_values),
        lambda children: st.dictionaries(_attr_keys, children),
        max_leaves=3,
    )


@st.composite
def variables(
    draw: st.DrawFn,
    *,
    array_strategy_fn: Union[ArrayStrategyFn, None] = None,
    dims: Union[
        st.SearchStrategy[Union[Sequence[Hashable], Mapping[Hashable, int]]],
        None,
    ] = None,
    dtype: st.SearchStrategy[np.dtype] = supported_dtypes(),
    attrs: st.SearchStrategy[Mapping] = attrs(),
) -> xr.Variable:
    """
    Generates arbitrary xarray.Variable objects.

    Follows the basic signature of the xarray.Variable constructor, but allows passing alternative strategies to
    generate either numpy-like array data or dimensions. Also allows specifying the shape or dtype of the wrapped array
    up front.

    Passing nothing will generate a completely arbitrary Variable (containing a numpy array).

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    array_strategy_fn: Callable which returns a strategy generating array-likes, optional
        Callable must accept shape and dtype kwargs, and must generate results consistent with its input.
        If not passed the default is to generate a small numpy array with one of the supported_dtypes.
    dims: Strategy for generating the dimensions, optional
        Can either be a strategy for generating a sequence of string dimension names,
        or a strategy for generating a mapping of string dimension names to integer lengths along each dimension.
        If provided as a mapping the array shape will be passed to array_strategy_fn.
        Default is to generate arbitrary dimension names for each axis in data.
    dtype: Strategy which generates np.dtype objects, optional
        Will be passed in to array_strategy_fn.
        Default is to generate any scalar dtype using supported_dtypes.
        Be aware that this default set of dtypes includes some not strictly allowed by the array API standard.
    attrs: Strategy which generates dicts, optional
        Default is to generate a nested attributes dictionary containing arbitrary strings, booleans, integers, Nones,
        and numpy arrays.

    Returns
    -------
    variable_strategy
        Strategy for generating xarray.Variable objects.

    Raises
    ------
    ValueError
        If a custom array_strategy_fn returns a strategy which generates an example array inconsistent with the shape
        & dtype input passed to it.

    Examples
    --------
    Generate completely arbitrary Variable objects backed by a numpy array:

    >>> variables().example()  # doctest: +SKIP
    <xarray.Variable (żō: 3)>
    array([43506,   -16,  -151], dtype=int32)
    >>> variables().example()  # doctest: +SKIP
    <xarray.Variable (eD: 4, ğŻżÂĕ: 2, T: 2)>
    array([[[-10000000., -10000000.],
            [-10000000., -10000000.]],

           [[-10000000., -10000000.],
            [        0., -10000000.]],

           [[        0., -10000000.],
            [-10000000.,        inf]],

           [[       -0., -10000000.],
            [-10000000.,        -0.]]], dtype=float32)
    Attributes:
        śřĴ:      {'ĉ': {'iĥſ': array([-30117,  -1740], dtype=int16)}}

    Generate only Variable objects with certain dimension names:

    >>> variables(dims=st.just(["a", "b"])).example()  # doctest: +SKIP
    <xarray.Variable (a: 5, b: 3)>
    array([[       248, 4294967295, 4294967295],
           [2412855555, 3514117556, 4294967295],
           [       111, 4294967295, 4294967295],
           [4294967295, 1084434988,      51688],
           [     47714,        252,      11207]], dtype=uint32)

    Generate only Variable objects with certain dimension names and lengths:

    >>> variables(dims=st.just({"a": 2, "b": 1})).example()  # doctest: +SKIP
    <xarray.Variable (a: 2, b: 1)>
    array([[-1.00000000e+007+3.40282347e+038j],
           [-2.75034266e-225+2.22507386e-311j]])
    """

    if any(
        not isinstance(arg, st.SearchStrategy) and arg is not None
        for arg in [dims, dtype, attrs]
    ):
        raise TypeError(
            "Contents dims, dtype, and attrs must each be provided as a hypothesis.strategies.SearchStrategy object (or None)."
            "To specify fixed contents, use hypothesis.strategies.just()."
        )

    _array_strategy_fn: ArrayStrategyFn
    array_strategy: st.SearchStrategy[T_DuckArray]
    if array_strategy_fn is None:
        _array_strategy_fn = smallish_arrays  # type: ignore[assignment]
    elif not callable(array_strategy_fn):
        raise TypeError(
            "array_strategy_fn must be a Callable that accepts the kwargs dtype and shape and returns a hypothesis "
            "strategy which generates corresponding array-like objects."
        )
    else:
        _array_strategy_fn = (
            array_strategy_fn  # satisfy mypy that this new variable cannot be None
        )

    _dtype = draw(dtype)

    if dims is not None:
        # generate dims first then draw data to match
        _dims = draw(dims)
        if isinstance(_dims, Sequence):
            dim_names = list(_dims)
            valid_shapes = npst.array_shapes(min_dims=len(_dims), max_dims=len(_dims))
            _shape = draw(valid_shapes)
            array_strategy = _array_strategy_fn(shape=_shape, dtype=_dtype)
        elif isinstance(_dims, (Mapping, dict)):
            # should be a mapping of form {dim_names: lengths}
            dim_names, _shape = list(_dims.keys()), tuple(_dims.values())
            array_strategy = _array_strategy_fn(shape=_shape, dtype=_dtype)
        else:
            raise TypeError(
                f"Invalid type returned by dims strategy - drew an object of type {type(dims)}"
            )
    else:
        # nothing provided, so generate everything consistently
        # We still generate the shape first here just so that we always pass shape to array_strategy_fn
        _shape = draw(npst.array_shapes())
        array_strategy = _array_strategy_fn(shape=_shape, dtype=_dtype)
        dim_names = draw(dimension_names(min_dims=len(_shape), max_dims=len(_shape)))

    _data = draw(array_strategy)

    if _data.shape != _shape:
        raise ValueError(
            "array_strategy_fn returned an array object with a different shape than it was passed."
            f"Passed {_shape}, but returned {_data.shape}."
            "Please either specify a consistent shape via the dims kwarg or ensure the array_strategy_fn callable "
            "obeys the shape argument passed to it."
        )
    if _data.dtype != _dtype:
        raise ValueError(
            "array_strategy_fn returned an array object with a different dtype than it was passed."
            f"Passed {_dtype}, but returned {_data.dtype}"
            "Please either specify a consistent dtype via the dtype kwarg or ensure the array_strategy_fn callable "
            "obeys the dtype argument passed to it."
        )

    return xr.Variable(dims=dim_names, data=_data, attrs=draw(attrs))


@st.composite
def unique_subset_of(
    draw: st.DrawFn,
    d: dict[Hashable, Any],
    *,
    min_size: int = 0,
    max_size: Union[int, None] = None,
) -> Mapping[Hashable, Any]:
    """
    Return a strategy which generates a unique subset of the given mapping.

    Each entry in the output subset will have a unique key.

    Requires the hypothesis package to be installed.

    Parameters
    ----------
    d: Mapping[Hashable, Any]
        Mapping from which to sample to produce the subset.
    min_size: int, optional
        Minimum size of the returned subset. Default is 0.
    max_size: int, optional
        Maximum size of the returned subset. Default is the full length of the input.
        If set to 0 the result will be an empty mapping.

    Returns
    -------
    unique_subset_strategy

    Examples
    --------
    >>> unique_subset_of({"x": 2, "y": 3}).example()  # doctest: +SKIP
    {'y': 3}
    """
    if not isinstance(d, dict):
        raise TypeError(
            f"Object to sample from must be a dict, but received type {type(d)}"
        )

    if len(d) == 0:
        raise ValueError("Can't sample from a length-zero sequence.")

    # TODO generalize this to work for any iterable? Could then be used on dimension_names as well as dimension_sizes.
    subset_keys = draw(
        st.lists(
            st.sampled_from(list(d.keys())),
            unique=True,
            min_size=min_size,
            max_size=max_size,
        )
    )
    return {k: d[k] for k in subset_keys}
