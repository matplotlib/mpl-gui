"""State and logic to promote a Figure -> a GUI window."""

import threading
import itertools

import matplotlib as mpl
from matplotlib import is_interactive
from matplotlib.cbook import _api
from matplotlib.backend_bases import FigureCanvasBase
from ._manage_backend import current_backend_module


_figure_count = itertools.count()


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


def promote_figure(fig, *, auto_draw=True, num):
    """Create a new figure manager instance."""
    _backend_mod = current_backend_module()
    if (
        getattr(_backend_mod.FigureCanvas, "required_interactive_framework", None)
        and threading.current_thread() is not threading.main_thread()
    ):
        _api.warn_external(
            "Starting a Matplotlib GUI outside of the main thread will likely fail."
        )

    if fig.canvas.manager is not None:
        if not isinstance(fig.canvas.manager, _backend_mod.FigureManager):
            raise Exception("Figure already has a manager an it is the wrong type!")
        else:
            # TODO is this the right behavior?
            return fig.canvas.manager
    # TODO: do we want to make sure we poison / destroy / decouple the existing
    # canavs?
    next_num = next(_figure_count)
    manager = _backend_mod.new_figure_manager_given_figure(
        num if num is not None else next_num, fig
    )
    if fig.get_label():
        manager.set_window_title(fig.get_label())

    if auto_draw:
        fig.stale_callback = _auto_draw_if_interactive

    if is_interactive():
        manager.show()
        fig.canvas.draw_idle()

    # HACK: the callback in backend_bases uses GCF.destroy which misses these
    # figures by design!
    def _destroy_on_hotkey(event):
        if event.key in mpl.rcParams["keymap.quit"]:
            # grab the manager off the event
            mgr = event.canvas.manager
            if mgr is None:
                raise RuntimeError("Should never be here, please report a bug.")
            # close the window
            mgr.destroy()

    # remove this callback.  Callbacks live on the Figure so survive the canvas
    # being replaced.
    fig._destroy_cid = fig.canvas.mpl_connect("key_press_event", _destroy_on_hotkey)

    return manager


def demote_figure(fig):
    """Fully clear all GUI elements from the `~matplotlib.figure.Figure`.

    The opposite of what is done during `mpl_gui.display`.

    Parameters
    ----------
    fig : matplotlib.figure.Figure

    """
    fig.canvas.destroy()
    fig.canvas.manager = None
    original_dpi = getattr(fig, "_original_dpi", fig.dpi)
    if (cid := getattr(fig, '_destroy_cid', None)) is not None:
        fig.canvas.mpl_disconnect(cid)
    FigureCanvasBase(fig)
    fig.dpi = original_dpi

    return fig
