import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


def test_axes3d_respects_set_visible_false():
    fig = Figure(figsize=(4, 2), dpi=100)
    canvas = FigureCanvasAgg(fig)

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')

    ax1.scatter([1], [1], [1])
    ax2.scatter([1], [1], [1], c='r')

    # Hide left axes entirely.
    ax1.set_visible(False)

    # Draw and examine pixels.
    canvas.draw()
    im = np.asarray(canvas.buffer_rgba())

    # Use a margin to avoid antialiasing artifacts at figure edges.
    h, w, _ = im.shape
    margin = 5
    left_half = im[margin:-margin, margin:w // 2 - margin, :3]

    # Background is typically uniform; sample a corner pixel.
    bg = im[margin, margin, :3]

    # Assert that the left half contains only background pixels.
    assert np.all(left_half == bg)
