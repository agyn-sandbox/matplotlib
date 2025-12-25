import warnings

import numpy as np
import numpy.ma as ma
import numpy.testing as npt

warnings.filterwarnings(
    "ignore",
    message=r"^'parseString' deprecated - use 'parse_string'",
    category=DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"^'resetCache' deprecated - use 'reset_cache'",
    category=DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"^'enablePackrat' deprecated - use 'enable_packrat'",
    category=DeprecationWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"^pkg_resources is deprecated as an API.",
    category=UserWarning,
)
warnings.filterwarnings(
    "ignore",
    message=(
        r"^Deprecated call to "
        r"`pkg_resources\.declare_namespace\('mpl_toolkits'\)`"
    ),
    category=DeprecationWarning,
)

import matplotlib  # noqa: E402

matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import colors  # noqa: E402


def _call_without_deprecation(func, *args, **kwargs):
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        return func(*args, **kwargs)


def test_colormap_uint8_empty_no_deprecation():
    cmap = plt.get_cmap()
    data = np.empty((0,), dtype=np.uint8)
    result = _call_without_deprecation(cmap, data)
    assert result.shape == (0, 4)


def test_colormap_uint8_matches_int():
    cmap = matplotlib.colormaps["viridis"]
    values_uint8 = np.array([0, 255], dtype=np.uint8)
    values_int = values_uint8.astype(int)

    result_uint8 = _call_without_deprecation(cmap, values_uint8)
    result_int = _call_without_deprecation(cmap, values_int)

    npt.assert_allclose(result_uint8, result_int)


def test_colormap_wide_unsigned_matches_int():
    cmap = matplotlib.colormaps["viridis"]
    dtypes = (np.uint16, np.uint32)

    for dtype in dtypes:
        values = np.array(
            [0, 10, np.iinfo(dtype).max],
            dtype=dtype,
        )
        result_unsigned = _call_without_deprecation(cmap, values)
        result_int = _call_without_deprecation(
            cmap,
            values.astype(np.int64),
        )
        npt.assert_allclose(result_unsigned, result_int)


def test_colormap_masked_uint8_bad_color():
    cmap = matplotlib.colormaps["viridis"].with_extremes(
        bad=(1, 0, 0, 1)
    )
    data = ma.array([1, 2], mask=[True, False], dtype=np.uint8)

    result = _call_without_deprecation(cmap, data)

    expected_good = _call_without_deprecation(
        cmap, np.array([2], dtype=int)
    )[0]
    npt.assert_array_equal(result[0], cmap.get_bad())
    npt.assert_array_equal(result[1], expected_good)


def test_colormap_signed_indices_over_under():
    base = colors.ListedColormap(
        [(0.1, 0.2, 0.3, 1.0), (0.4, 0.5, 0.6, 1.0)], name="test-listed"
    )
    cmap = base.with_extremes(
        under=(1.0, 0.0, 0.0, 1.0),
        over=(0.0, 1.0, 0.0, 1.0),
    )

    values = np.array([-1, 0, 256], dtype=np.int16)

    result = _call_without_deprecation(cmap, values)

    good = _call_without_deprecation(
        cmap, np.array([0], dtype=int)
    )[0]
    npt.assert_array_equal(result[0], cmap.get_under())
    npt.assert_array_equal(result[1], good)
    npt.assert_array_equal(result[2], cmap.get_over())
