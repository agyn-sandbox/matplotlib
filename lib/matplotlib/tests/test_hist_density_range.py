import numpy as np
import pytest

from matplotlib import pyplot as plt


def _assert_bin_range(bins, expected_range=(0, 1)):
    assert bins[0] == pytest.approx(expected_range[0])
    assert bins[-1] == pytest.approx(expected_range[1])


@pytest.mark.parametrize("density", [False, True])
def test_hist_preserves_range_auto_single_dataset(density):
    fig, ax = plt.subplots()
    try:
        data = np.array([0.05, 0.15, 0.35, 0.65, 0.85])
        _, bins, _ = ax.hist(
            data,
            bins="auto",
            range=(0, 1),
            density=density,
        )
    finally:
        plt.close(fig)

    _assert_bin_range(bins)


@pytest.mark.parametrize("density", [False, True])
def test_hist_preserves_range_int_bins_single_dataset(density):
    fig, ax = plt.subplots()
    try:
        data = np.array([0.05, 0.25, 0.45, 0.65, 0.85])
        _, bins, _ = ax.hist(
            data,
            bins=5,
            range=(0, 1),
            density=density,
        )
    finally:
        plt.close(fig)

    _assert_bin_range(bins)


@pytest.mark.parametrize("density", [False, True])
def test_hist_preserves_range_multiple_datasets(density):
    fig, ax = plt.subplots()
    try:
        datasets = (
            np.array([0.05, 0.15, 0.25, 0.35]),
            np.array([0.55, 0.65, 0.75, 0.85]),
        )
        _, bins, _ = ax.hist(
            datasets,
            bins="auto",
            range=(0, 1),
            density=density,
        )
    finally:
        plt.close(fig)

    _assert_bin_range(bins)


def test_hist_preserves_range_with_weights_density_true():
    fig, ax = plt.subplots()
    try:
        data = np.array([0.1, 0.3, 0.6, 0.9])
        weights = np.array([1.0, 0.5, 2.0, 1.5])
        _, bins, _ = ax.hist(
            data,
            # numpy disallows automatic bin selection when weights are used.
            bins=5,
            range=(0, 1),
            weights=weights,
            density=True,
        )
    finally:
        plt.close(fig)

    _assert_bin_range(bins)
