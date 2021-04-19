"""Helpers to create new Figures."""

from ._figure import Figure
from ._promotion import promote_figure


def figure(
    *,
    label=None,  # autoincrement if None, else integer from 1-N
    figsize=None,  # defaults to rc figure.figsize
    dpi=None,  # defaults to rc figure.dpi
    facecolor=None,  # defaults to rc figure.facecolor
    edgecolor=None,  # defaults to rc figure.edgecolor
    frameon=True,
    FigureClass=Figure,
    clear=False,
    auto_draw=True,
    **kwargs,
):
    """
    Create a new figure

    Parameters
    ----------
    label : str, optional
        Label for the figure.  Will be used as the window title

    figsize : (float, float), default: :rc:`figure.figsize`
        Width, height in inches.

    dpi : float, default: :rc:`figure.dpi`
        The resolution of the figure in dots-per-inch.

    facecolor : color, default: :rc:`figure.facecolor`
        The background color.

    edgecolor : color, default: :rc:`figure.edgecolor`
        The border color.

    frameon : bool, default: True
        If False, suppress drawing the figure frame.

    FigureClass : subclass of `~matplotlib.figure.Figure`
        Optionally use a custom `.Figure` instance.

    tight_layout : bool or dict, default: :rc:`figure.autolayout`
        If ``False`` use *subplotpars*. If ``True`` adjust subplot
        parameters using `.tight_layout` with default padding.
        When providing a dict containing the keys ``pad``, ``w_pad``,
        ``h_pad``, and ``rect``, the default `.tight_layout` paddings
        will be overridden.

    constrained_layout : bool, default: :rc:`figure.constrained_layout.use`
        If ``True`` use constrained layout to adjust positioning of plot
        elements.  Like ``tight_layout``, but designed to be more
        flexible.  See
        :doc:`/tutorials/intermediate/constrainedlayout_guide`
        for examples.  (Note: does not work with `add_subplot` or
        `~.pyplot.subplot2grid`.)

    **kwargs : optional
        See `~.matplotlib.figure.Figure` for other possible arguments.

    Returns
    -------
    `~matplotlib.figure.Figure`
        The `.Figure` instance returned will also be passed to
        new_figure_manager in the backends, which allows to hook custom
        `.Figure` classes into the pyplot interface. Additional kwargs will be
        passed to the `.Figure` init function.

    """

    fig = FigureClass(
        label=label,
        figsize=figsize,
        dpi=dpi,
        facecolor=facecolor,
        edgecolor=edgecolor,
        frameon=frameon,
        FigureClass=FigureClass,
        auto_draw=auto_draw,
        **kwargs,
    )
    promote_figure(fig)
    return fig
