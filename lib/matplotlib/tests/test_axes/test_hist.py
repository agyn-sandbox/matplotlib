from __future__ import annotations

import numpy as np
import pytest

import matplotlib.pyplot as plt


def _generate_density_samples(
    *,
    seed: int = 20250101,
    size: int = 100_000,
    scale: float = 1.2,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.standard_normal(size) * scale


def _hist_peak_and_ylim(
    histtype: str, values: np.ndarray,
) -> tuple[float, float]:
    fig, ax = plt.subplots()
    try:
        counts, _, _ = ax.hist(
            values,
            bins=100,
            density=True,
            histtype=histtype,
        )
        peak = float(counts.max()) if counts.size else 0.0
        upper = float(ax.get_ylim()[1])
    finally:
        plt.close(fig)
    return peak, upper


def test_hist_step_density_autoscale_includes_peak() -> None:
    values = _generate_density_samples()
    peak, upper = _hist_peak_and_ylim("step", values)
    assert upper >= peak


def test_hist_step_density_scale_invariance() -> None:
    values = _generate_density_samples()
    peak_base, upper_base = _hist_peak_and_ylim("step", values)
    scaled_values = values * 3.0
    peak_scaled, upper_scaled = _hist_peak_and_ylim("step", scaled_values)

    assert upper_base >= peak_base
    assert upper_scaled >= peak_scaled

    ratio_base = upper_base / peak_base
    ratio_scaled = upper_scaled / peak_scaled
    assert ratio_scaled == pytest.approx(ratio_base, rel=0.05)


def test_hist_stepfilled_density_autoscale_includes_peak() -> None:
    values = _generate_density_samples()
    peak, upper = _hist_peak_and_ylim("stepfilled", values)
    assert upper >= peak
