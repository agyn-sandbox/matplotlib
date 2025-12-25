Per-artist text antialiasing control
------------------------------------

`.Text` instances now expose :meth:`~matplotlib.text.Text.set_antialiased`
and :meth:`~matplotlib.text.Text.get_antialiased`, allowing text artists to
override the global :rc:`text.antialiased` setting on a per-artist basis. The
new preference is propagated through `GraphicsContextBase` so backends such as
Agg and Cairo honor the per-text value.
