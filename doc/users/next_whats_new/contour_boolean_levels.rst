Boolean contour defaults
------------------------

`.Axes.contour` and `.Axes.contourf` now recognise boolean input arrays when
``levels`` is omitted. Line contours default to a single threshold at ``0.5``
while filled contours draw the three regions ``[0.0, 0.5, 1.0]`` to
distinguish ``False`` and ``True`` values. Passing explicit ``levels``, using a
custom locator, or enabling logarithmic scaling continues to behave exactly as
before.
