import importlib
import itertools
import logging
import threading
import sys

from matplotlib import cbook, rcsetup
from matplotlib import rcParamsOrig, rcParams, rcParamsDefault
from matplotlib import is_interactive, interactive as _interactive
from matplotlib.cbook import _api
from matplotlib.figure import Figure

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


_log = logging.getLogger(__name__)

_figure_count = itertools.count()


def _get_required_interactive_framework(backend_mod):
    return getattr(backend_mod.FigureCanvas, "required_interactive_framework", None)


def switch_backend(newbackend):
    """
    Close all open figures and set the Matplotlib backend.

    The argument is case-insensitive.  Switching to an interactive backend is
    possible only if no event loop for another interactive backend has started.
    Switching to and from non-interactive backends is always possible.

    Parameters
    ----------
    newbackend : str
        The name of the backend to use.
    """
    global _backend_mod
    # make sure the init is pulled up so we can assign to it later
    import matplotlib.backends

    if newbackend is rcsetup._auto_backend_sentinel:
        current_framework = cbook._get_running_interactive_framework()
        mapping = {
            "qt5": "qt5agg",
            "qt4": "qt4agg",
            "gtk3": "gtk3agg",
            "wx": "wxagg",
            "tk": "tkagg",
            "macosx": "macosx",
            "headless": "agg",
        }

        best_guess = mapping.get(current_framework, None)
        if best_guess is not None:
            candidates = [best_guess]
        else:
            candidates = []
        candidates += ["macosx", "qt5agg", "gtk3agg", "tkagg", "wxagg"]

        # Don't try to fallback on the cairo-based backends as they each have
        # an additional dependency (pycairo) over the agg-based backend, and
        # are of worse quality.
        for candidate in candidates:
            try:
                switch_backend(candidate)
            except ImportError:
                continue
            else:
                rcParamsOrig["backend"] = candidate
                return
        else:
            # Switching to Agg should always succeed; if it doesn't, let the
            # exception propagate out.
            switch_backend("agg")
            rcParamsOrig["backend"] = "agg"
            return

    # Backends are implemented as modules, but "inherit" default method
    # implementations from backend_bases._Backend.  This is achieved by
    # creating a "class" that inherits from backend_bases._Backend and whose
    # body is filled with the module's globals.

    backend_name = cbook._backend_module_name(newbackend)

    class backend_mod(matplotlib.backend_bases._Backend):
        locals().update(vars(importlib.import_module(backend_name)))

    required_framework = _get_required_interactive_framework(backend_mod)
    if required_framework is not None:
        current_framework = cbook._get_running_interactive_framework()
        if (
            current_framework
            and required_framework
            and current_framework != required_framework
        ):
            raise ImportError(
                "Cannot load backend {!r} which requires the {!r} interactive "
                "framework, as {!r} is currently running".format(
                    newbackend, required_framework, current_framework
                )
            )

    _log.debug("Loaded backend %s version %s.", newbackend, backend_mod.backend_version)

    rcParams["backend"] = rcParamsDefault["backend"] = newbackend
    _backend_mod = backend_mod

    # is IPython imported?
    mod_ipython = sys.modules.get("IPython")
    if mod_ipython:
        # if so are we in an IPython session
        ip = mod_ipython.get_ipython()
        if ip:
            ip.enable_gui(required_framework)


def _warn_if_gui_out_of_main_thread():
    if (
        _get_required_interactive_framework(_backend_mod)
        and threading.current_thread() is not threading.main_thread()
    ):
        _api.warn_external(
            "Starting a Matplotlib GUI outside of the main thread will likely fail."
        )


def new_figure_manager(*args, fig_cls=Figure, **kwargs):
    """Create a new figure manager instance."""
    # TODO make Figure handle kwargs like everything else!
    label = kwargs.pop("label", None)
    fig = fig_cls(*args, **kwargs)
    if label is not None:
        fig.set_label(label)
    return promote_figure(fig)


def promote_figure(fig, *, auto_draw=True):
    """Create a new figure manager instance."""
    _warn_if_gui_out_of_main_thread()
    canvas = _backend_mod.FigureCanvas(fig)
    manager = _backend_mod.FigureManager(canvas, next(_figure_count))
    if fig.get_label():
        manager.set_window_title(fig.get_label())

    if auto_draw:
        fig.stale_callback = _auto_draw_if_interactive

    if is_interactive():
        manager.show()
        fig.canvas.draw_idle()

    return manager


def show(figs, *, block=None, timeout=0):
    # TODO handle single figure
    managers = []
    for fig in figs:
        if fig.canvas.manager is not None:
            managers.append(fig.canvas.manager)
        else:
            managers.append(promote_figure(fig))

    for manager in managers:
        manager.show()

    if block is None:
        block = not is_interactive()

    if block:
        # TODO expose the main loop more elegantly!
        # TODO make main
        _backend_mod.Show().mainloop()


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

    return new_figure_manager(
        label=label,
        figsize=figsize,
        dpi=dpi,
        facecolor=facecolor,
        edgecolor=edgecolor,
        frameon=frameon,
        FigureClass=FigureClass,
        auto_draw=auto_draw,
        **kwargs,
    ).canvas.figure


class _IoffContext:
    """
    Context manager for `.ioff`.

    The state is changed in ``__init__()`` instead of ``__enter__()``. The
    latter is a no-op. This allows using `.ioff` both as a function and
    as a context.
    """

    def __init__(self):
        self.wasinteractive = is_interactive()
        _interactive(False)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if self.wasinteractive:
            _interactive(True)
        else:
            _interactive(False)


class _IonContext:
    """
    Context manager for `.ion`.

    The state is changed in ``__init__()`` instead of ``__enter__()``. The
    latter is a no-op. This allows using `.ion` both as a function and
    as a context.
    """

    def __init__(self):
        self.wasinteractive = is_interactive()
        _interactive(True)

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.wasinteractive:
            _interactive(False)
        else:
            _interactive(True)


def ioff():
    """
    Disable interactive mode.

    See `.pyplot.isinteractive` for more details.

    See Also
    --------
    ion : Enable interactive mode.
    isinteractive : Whether interactive mode is enabled.
    show : Show all figures (and maybe block).
    pause : Show all figures, and block for a time.

    Notes
    -----
    For a temporary change, this can be used as a context manager::

        # if interactive mode is on
        # then figures will be shown on creation
        plt.ion()
        # This figure will be shown immediately
        fig = plt.figure()

        with plt.ioff():
            # interactive mode will be off
            # figures will not automatically be shown
            fig2 = plt.figure()
            # ...

    To enable usage as a context manager, this function returns an
    ``_IoffContext`` object. The return value is not intended to be stored
    or accessed by the user.
    """
    return _IoffContext()


def ion():
    """
    Enable interactive mode.

    See `.pyplot.isinteractive` for more details.

    See Also
    --------
    ioff : Disable interactive mode.
    isinteractive : Whether interactive mode is enabled.
    show : Show all figures (and maybe block).
    pause : Show all figures, and block for a time.

    Notes
    -----
    For a temporary change, this can be used as a context manager::

        # if interactive mode is off
        # then figures will not be shown on creation
        plt.ioff()
        # This figure will not be shown immediately
        fig = plt.figure()

        with plt.ion():
            # interactive mode will be on
            # figures will automatically be shown
            fig2 = plt.figure()
            # ...

    To enable usage as a context manager, this function returns an
    ``_IonContext`` object. The return value is not intended to be stored
    or accessed by the user.
    """
    return _IonContext()


def _auto_draw_if_interactive(fig, val):
    """
    An internal helper function for making sure that auto-redrawing
    works as intended in the plain python repl.

    Parameters
    ----------
    fig : Figure
        A figure object which is assumed to be associated with a canvas
    """
    if (
        val
        and is_interactive()
        and not fig.canvas.is_saving()
        and not fig.canvas._is_idle_drawing
    ):
        # Some artists can mark themselves as stale in the middle of drawing
        # (e.g. axes position & tick labels being computed at draw time), but
        # this shouldn't trigger a redraw because the current redraw will
        # already take them into account.
        with fig.canvas._idle_draw_cntx():
            fig.canvas.draw_idle()


# set up the backend!
switch_backend(rcParams["backend"])
