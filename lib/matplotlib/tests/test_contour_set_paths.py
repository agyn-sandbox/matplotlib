import numpy as np
import pytest

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.transforms import Affine2D


def _sample_data():
    x = np.linspace(-1, 1, 5)
    y = np.linspace(-1, 1, 5)
    X, Y = np.meshgrid(x, y)
    Z = np.hypot(X, Y)
    return X, Y, Z


def test_set_paths_replaces_paths_and_clears_split_cache():
    X, Y, Z = _sample_data()
    fig, ax = plt.subplots()
    try:
        cs = ax.contour(X, Y, Z, levels=[0.5, 1.0, 1.5])
        with pytest.warns(mpl.MatplotlibDeprecationWarning):
            _ = cs.collections
        assert hasattr(cs, "_old_style_split_collections")

        new_paths = [Path(p.vertices.copy(), p.codes) for p in cs.get_paths()]

        cs.stale = False
        cs.set_paths(new_paths)

        assigned_paths = cs.get_paths()
        assert assigned_paths is not new_paths
        assert len(assigned_paths) == len(new_paths)
        assert all(a is b for a, b in zip(assigned_paths, new_paths))
        assert cs.stale
        assert not hasattr(cs, "_old_style_split_collections")
    finally:
        plt.close(fig)


def test_set_paths_allows_transformed_labeling():
    X, Y, Z = _sample_data()
    fig, ax = plt.subplots()
    try:
        cs = ax.contour(X, Y, Z, levels=[0.5, 1.0, 1.5])

        original_paths = list(cs.get_paths())
        if original_paths:
            original_vertices = np.concatenate(
                [p.vertices for p in original_paths if len(p.vertices)], axis=0
            )
        else:
            pytest.skip("Contour generator returned no paths")

        dx, dy = 2.0, -1.0
        transform = Affine2D().translate(dx, dy)
        transformed_paths = [transform.transform_path(path) for path in original_paths]

        cs.set_paths(transformed_paths)
        labels = cs.clabel(cs.levels)

        assert labels

        vertices = np.concatenate(
            [p.vertices for p in transformed_paths if len(p.vertices)], axis=0
        )
        min_x, min_y = vertices.min(axis=0)
        max_x, max_y = vertices.max(axis=0)

        np.testing.assert_allclose(min_x, original_vertices[:, 0].min() + dx)
        np.testing.assert_allclose(max_x, original_vertices[:, 0].max() + dx)
        np.testing.assert_allclose(min_y, original_vertices[:, 1].min() + dy)
        np.testing.assert_allclose(max_y, original_vertices[:, 1].max() + dy)

        for label in labels:
            x_pos, y_pos = label.get_position()
            assert min_x <= x_pos <= max_x
            assert min_y <= y_pos <= max_y
    finally:
        plt.close(fig)


def test_behavior_matches_when_not_using_set_paths():
    X, Y, Z = _sample_data()

    fig_default, ax_default = plt.subplots()
    try:
        cs_default = ax_default.contour(X, Y, Z, levels=[0.5, 1.0, 1.5])
        manual_positions = [tuple(path.vertices[len(path.vertices) // 2])
                            for path in cs_default.get_paths() if len(path.vertices)]
        if not manual_positions:
            pytest.skip("Contour generator returned no paths")
        default_labels = cs_default.clabel(
            cs_default.levels, manual=manual_positions.copy()
        )
        default_positions = np.array([label.get_position() for label in default_labels])
    finally:
        plt.close(fig_default)

    fig_copy, ax_copy = plt.subplots()
    try:
        cs_copy = ax_copy.contour(X, Y, Z, levels=[0.5, 1.0, 1.5])
        copied_paths = [Path(p.vertices.copy(), p.codes) for p in cs_copy.get_paths()]
        cs_copy.set_paths(copied_paths)
        copied_labels = cs_copy.clabel(
            cs_copy.levels, manual=manual_positions.copy()
        )
        copied_positions = np.array([label.get_position() for label in copied_labels])
    finally:
        plt.close(fig_copy)

    np.testing.assert_allclose(copied_positions, default_positions)
