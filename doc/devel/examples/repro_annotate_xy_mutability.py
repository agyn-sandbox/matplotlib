"""Reproduction script for annotation xy mutability regression (Issue #72).

Run this module to observe how mutating the original ``xy`` or ``xytext``
arrays changes the rendered annotation position. On affected builds the
rendered position drifts to the mutated coordinates after the redraw.
"""

import matplotlib


matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


def main() -> None:
    fig, ax = plt.subplots(layout="constrained")

    xy = np.array([0.25, 0.75], dtype=float)
    xytext = np.array([24.0, -12.0], dtype=float)

    annotation = ax.annotate(
        "Mutable source demo",
        xy=xy,
        xytext=xytext,
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->"),
    )

    def snapshot(tag: str) -> None:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        xy_pixels = annotation._get_position_xy(renderer)
        print(f"{tag} annotation xy (data): {annotation.xy}")
        print(f"{tag} annotation xy in pixels: {xy_pixels}")
        print(f"{tag} annotation xytext (offset points): {annotation.get_position()}")

    snapshot("Initial")

    xy[:] = [0.6, 0.2]
    xytext[:] = [-18.0, 30.0]

    snapshot("After mutation")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Annotation mutability reproduction")
    fig.savefig("repro_annotate_xy_mutability.png", dpi=150)


if __name__ == "__main__":
    main()
