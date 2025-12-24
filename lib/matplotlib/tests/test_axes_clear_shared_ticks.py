import matplotlib as mpl
import matplotlib.pyplot as plt


def test_clear_respects_tick_side_defaults():
    with mpl.rc_context({
        "xtick.top": False,
        "ytick.right": False,
        "xtick.minor.top": False,
        "ytick.minor.right": False,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
    }):
        fig, ax = plt.subplots()
        try:
            ax.plot([0, 1], [0, 1])
            ax.clear()
            ax.plot([0, 1], [0, 1])
            ax.minorticks_on()
            fig.canvas.draw()

            assert all(
                not tick.tick2line.get_visible()
                for tick in ax.xaxis.get_major_ticks()
            )
            assert all(
                not tick.tick2line.get_visible()
                for tick in ax.yaxis.get_major_ticks()
            )
            x_minor = ax.xaxis.get_minor_ticks()
            assert x_minor
            assert all(
                not tick.tick2line.get_visible()
                for tick in x_minor
            )
            y_minor = ax.yaxis.get_minor_ticks()
            assert y_minor
            assert all(
                not tick.tick2line.get_visible()
                for tick in y_minor
            )
        finally:
            plt.close(fig)


def test_clear_shared_axes_hide_interior_labels():
    fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
    try:
        for ax in axes.flat:
            ax.clear()
            ax.plot([0, 1], [0, 1])

        fig.canvas.draw()

        nrows, ncols = axes.shape
        for idx, ax in enumerate(axes.flat):
            row, col = divmod(idx, ncols)
            x_label_vis = [tick.label1.get_visible()
                           for tick in ax.xaxis.get_major_ticks()]
            y_label_vis = [tick.label1.get_visible()
                           for tick in ax.yaxis.get_major_ticks()]

            assert x_label_vis
            assert y_label_vis

            if row < nrows - 1:
                assert all(not vis for vis in x_label_vis)
            else:
                assert any(x_label_vis)

            if col > 0:
                assert all(not vis for vis in y_label_vis)
            else:
                assert any(y_label_vis)
    finally:
        plt.close(fig)
