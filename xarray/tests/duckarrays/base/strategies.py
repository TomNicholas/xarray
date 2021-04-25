import hypothesis.extra.numpy as npst
import hypothesis.strategies as st

import xarray as xr


def shapes(ndim):
    return npst.array_shapes(min_dims=ndim, max_dims=ndim)


dtypes = (
    npst.integer_dtypes()
    | npst.unsigned_integer_dtypes()
    | npst.floating_dtypes()
    | npst.complex_number_dtypes()
)


def numpy_array(shape):
    return npst.arrays(dtype=dtypes, shape=shape)


@st.composite
def variable(draw, create_data, *, sizes=None):
    if sizes is not None:
        dims, shape = zip(*draw(sizes).items())
    else:
        dims = draw(st.lists(st.text(min_size=1), max_size=4, unique=True).map(tuple))
        ndim = len(dims)
        shape = draw(shapes(ndim))

    data = draw(create_data(shape))
    return xr.Variable(dims, data)


@st.composite
def data_array(draw, create_data):
    name = draw(st.none() | st.text(min_size=1))

    dims = draw(st.lists(elements=st.text(min_size=1), max_size=4, unique=True))
    shape = draw(shapes(len(dims)))

    data = draw(create_data(shape))

    return xr.DataArray(
        data=data,
        name=name,
        dims=dims,
    )


def dimension_sizes(sizes):
    sizes_ = list(sizes.items())
    return st.lists(
        elements=st.sampled_from(sizes_), min_size=1, max_size=len(sizes_)
    ).map(dict)


@st.composite
def dataset(
    draw,
    create_data,
    *,
    min_dims=1,
    max_dims=4,
    min_size=2,
    max_size=5,
    min_vars=1,
    max_vars=5,
):
    names = st.text(min_size=1)
    sizes = st.dictionaries(
        keys=names,
        values=st.integers(min_value=min_size, max_value=max_size),
        min_size=min_dims,
        max_size=max_dims,
    )

    data_vars = sizes.flatmap(
        lambda s: st.dictionaries(
            keys=names.filter(lambda n: n not in s),
            values=variable(create_data, sizes=dimension_sizes(s)),
            min_size=min_vars,
            max_size=max_vars,
        )
    )

    return xr.Dataset(data_vars=draw(data_vars))


def valid_axis(ndim):
    if ndim == 0:
        return st.none() | st.just(0)
    return st.none() | st.integers(-ndim, ndim - 1)


def valid_axes(ndim):
    return valid_axis(ndim) | npst.valid_tuple_axes(ndim)
