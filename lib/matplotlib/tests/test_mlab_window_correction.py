import numpy as np
import pytest
from numpy.testing import assert_allclose

from matplotlib import mlab


pytestmark = pytest.mark.filterwarnings(
    "ignore:'enablePackrat' deprecated - use 'enable_packrat':DeprecationWarning"
)


_FS = 1024.0
_NFFT = 512
_F0 = 128.0


def _test_signal():
    t = np.arange(_NFFT) / _FS
    return np.sin(2 * np.pi * _F0 * t)


def _negative_value_window_values(length):
    n = np.arange(length, dtype=float)
    return 0.5 + np.cos(2 * np.pi * n / (length - 1))


def _negative_value_window(segment):
    weights = _negative_value_window_values(segment.shape[0])
    return weights * segment


def _expected_psd(window_vals, scale_by_freq):
    segments = mlab._stride_windows(_test_signal(), _NFFT, noverlap=0)
    segments = mlab.detrend(segments, mlab.detrend_none, axis=0)
    windowed = segments * window_vals[:, None]

    fft = np.fft.fft(windowed, n=_NFFT, axis=0)
    num_freqs = _NFFT // 2 + 1
    fft = fft[:num_freqs, :]

    periodogram = np.conj(fft) * fft
    periodogram[1:-1] *= 2.0

    if scale_by_freq:
        periodogram /= _FS
        periodogram /= (np.abs(window_vals) ** 2).sum()
    else:
        periodogram /= (window_vals.sum()) ** 2

    return periodogram.mean(axis=1)


def test_psd_spectrum_uses_window_sum_square():
    window_vals = _negative_value_window_values(_NFFT)
    spectrum, freqs = mlab.psd(
        x=_test_signal(),
        NFFT=_NFFT,
        Fs=_FS,
        window=_negative_value_window,
        noverlap=0,
        pad_to=_NFFT,
        sides="onesided",
        scale_by_freq=False,
    )

    expected = _expected_psd(window_vals, scale_by_freq=False)
    assert_allclose(spectrum, expected, rtol=1e-12, atol=1e-12)


def test_psd_density_uses_window_energy_norm():
    window_vals = _negative_value_window_values(_NFFT)
    density, _ = mlab.psd(
        x=_test_signal(),
        NFFT=_NFFT,
        Fs=_FS,
        window=_negative_value_window,
        noverlap=0,
        pad_to=_NFFT,
        sides="onesided",
        scale_by_freq=True,
    )

    expected = _expected_psd(window_vals, scale_by_freq=True)
    assert_allclose(density, expected, rtol=1e-12, atol=1e-12)


def test_psd_density_spectrum_consistency():
    window_vals = _negative_value_window_values(_NFFT)
    density, freqs = mlab.psd(
        x=_test_signal(),
        NFFT=_NFFT,
        Fs=_FS,
        window=_negative_value_window,
        noverlap=0,
        pad_to=_NFFT,
        sides="onesided",
        scale_by_freq=True,
    )
    spectrum, _ = mlab.psd(
        x=_test_signal(),
        NFFT=_NFFT,
        Fs=_FS,
        window=_negative_value_window,
        noverlap=0,
        pad_to=_NFFT,
        sides="onesided",
        scale_by_freq=False,
    )

    lhs = density * (window_vals**2).sum()
    rhs = spectrum / _FS * (window_vals.sum()) ** 2
    assert_allclose(lhs, rhs, rtol=1e-12, atol=1e-12)
