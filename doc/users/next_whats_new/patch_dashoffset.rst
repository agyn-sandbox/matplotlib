Patch dash offsets honored on patches
-------------------------------------

Patches now respect the dash offset specified via
`~matplotlib.patches.Patch.set_linestyle`, so edge stroking matches the
behaviour of lines across both vector (e.g. SVG) and raster (Agg) backends.
