import pytest

from matplotlib.offsetbox import DrawingArea, HPacker, VPacker


class _UnitRenderer:
    def points_to_pixels(self, points):
        return points


@pytest.fixture()
def renderer():
    return _UnitRenderer()


def _y_offsets(offsets):
    return [y for _, y in offsets]


def _x_offsets(offsets):
    return [x for x, _ in offsets]


def test_hpacker_top_bottom(renderer):
    short = DrawingArea(1, 10)
    tall = DrawingArea(1, 30)

    pack_top = HPacker(children=[short, tall], align="top", pad=0., sep=0.)
    *_top, offsets_top = pack_top.get_extent_offsets(renderer)
    assert _y_offsets(offsets_top) == [20, 0]

    pack_bottom = HPacker(children=[DrawingArea(1, 10), DrawingArea(1, 30)],
                          align="bottom", pad=0., sep=0.)
    *_bottom, offsets_bottom = pack_bottom.get_extent_offsets(renderer)
    assert _y_offsets(offsets_bottom) == [0, 0]


def test_hpacker_center(renderer):
    short = DrawingArea(1, 10)
    tall = DrawingArea(1, 30)
    pack_center = HPacker(children=[short, tall], align="center",
                          pad=0., sep=0.)
    *_center, offsets_center = pack_center.get_extent_offsets(renderer)
    assert _y_offsets(offsets_center) == [10, 0]


def test_hpacker_baseline_descent(renderer):
    descender = DrawingArea(1, 10, ydescent=5)
    baseline = DrawingArea(1, 20, ydescent=0)
    pack_baseline = HPacker(children=[descender, baseline], align="baseline",
                            pad=0., sep=0.)

    width, height, xdescent, ydescent, offsets = (
        pack_baseline.get_extent_offsets(renderer))

    assert height == pytest.approx(25)
    assert ydescent == pytest.approx(5)
    assert _y_offsets(offsets) == [0, 0]


def test_vpacker_left_right(renderer):
    narrow = DrawingArea(10, 1)
    wide = DrawingArea(30, 1)

    pack_left = VPacker(children=[narrow, wide], align="left",
                         pad=0., sep=0.)
    *_left, offsets_left = pack_left.get_extent_offsets(renderer)
    assert _x_offsets(offsets_left) == [0, 0]

    pack_right = VPacker(children=[DrawingArea(10, 1), DrawingArea(30, 1)],
                          align="right", pad=0., sep=0.)
    *_right, offsets_right = pack_right.get_extent_offsets(renderer)
    assert _x_offsets(offsets_right) == [20, 0]
