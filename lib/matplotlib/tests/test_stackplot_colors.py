import warnings

import numpy as np
from cycler import cycler


def _import_pyplot_and_colors():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from matplotlib import colors as mcolors, pyplot as plt
    return mcolors, plt


mcolors, plt = _import_pyplot_and_colors()


def _stackplot_data(num_layers=3):
    x = np.arange(3)
    layers = [np.full_like(x, fill_value=i + 1, dtype=float)
              for i in range(num_layers)]
    return x, layers


def _facecolors(collections):
    return [tuple(coll.get_facecolors()[0]) for coll in collections]


def test_stackplot_accepts_cn_colors():
    fig, ax = plt.subplots()
    x, layers = _stackplot_data()

    collections = ax.stackplot(x, *layers, colors=['C2', 'C3', 'C4'])

    actual = _facecolors(collections)
    expected = [tuple(mcolors.to_rgba(color)) for color in ['C2', 'C3', 'C4']]
    assert actual == expected


def test_stackplot_does_not_mutate_axes_cycler():
    fig, (ax_left, ax_right) = plt.subplots(1, 2)
    x, layers = _stackplot_data(2)
    prop_colors = ['tab:blue', 'tab:orange', 'tab:green']
    ax_left.set_prop_cycle(color=prop_colors)
    ax_right.set_prop_cycle(color=prop_colors)

    ax_left.stackplot(x, *layers, colors=['C3', 'C4'])

    left_line, = ax_left.plot(x, x)
    right_line, = ax_right.plot(x, x)

    assert left_line.get_color() == right_line.get_color() == prop_colors[0]


def test_stackplot_colors_repeat_when_short():
    fig, ax = plt.subplots()
    x, layers = _stackplot_data(4)

    collections = ax.stackplot(x, *layers, colors=['C1'])

    actual = _facecolors(collections)
    expected_color = tuple(mcolors.to_rgba('C1'))
    assert actual == [expected_color] * len(layers)


def test_stackplot_colors_exact_match():
    fig, ax = plt.subplots()
    x, layers = _stackplot_data(3)
    requested = ['C5', 'C6', 'C7']

    collections = ax.stackplot(x, *layers, colors=requested)

    actual = _facecolors(collections)
    expected = [tuple(mcolors.to_rgba(color)) for color in requested]
    assert actual == expected


def test_stackplot_colors_stringlist_single_letters():
    fig, ax = plt.subplots()
    x, layers = _stackplot_data(3)

    collections = ax.stackplot(x, *layers, colors='rgb')

    actual = _facecolors(collections)
    expected = [tuple(mcolors.to_rgba(color)) for color in ['r', 'g', 'b']]
    assert actual == expected


def test_stackplot_uses_axes_cycler_when_colors_none():
    fig, ax = plt.subplots()
    x, layers = _stackplot_data(3)
    cycler_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    ax.set_prop_cycle(cycler(color=cycler_colors))

    collections = ax.stackplot(x, *layers)

    actual = _facecolors(collections)
    expected = [tuple(mcolors.to_rgba(color))
                for color in cycler_colors[:len(layers)]]
    assert actual == expected

    next_line, = ax.plot(x, x)
    assert next_line.get_color() == cycler_colors[len(layers)]
