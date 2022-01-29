"""
Prototype project for new Matplotlib GUI management.

The pyplot module current serves two critical, but unrelated functions:

1. provide a state-full implicit API that rhymes / was inspired by MATLAB
2. provide the management of interaction between Matplotlib and the GUI event
   loop

This project is prototype for separating the second function from the first.
This will enable users to both only use the explicit API (nee OO interface) and
to have smooth integration with the GUI event loop as with pyplot.

"""
import logging
import functools
from itertools import count

from matplotlib.backend_bases import FigureCanvasBase as _FigureCanvasBase

from ._figure import Figure  # noqa: F401

from ._manage_interactive import ion, ioff, is_interactive  # noqa: F401
from ._manage_backend import select_gui_toolkit  # noqa: F401
from ._manage_backend import current_backend_module as _cbm
from ._promotion import promote_figure as promote_figure
from ._creation import figure, subplots, subplot_mosaic  # noqa: F401

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


_log = logging.getLogger(__name__)


def show(figs, *, block=None, timeout=0):
    """
    Show the figures and maybe block.

    Parameters
    ----------
    figs : List[Figure]
        The figures to show.  If they do not currently have a GUI aware
        canvas + manager attached they will be promoted.

    block : bool, optional
        Whether to wait for all figures to be closed before returning.

        If `True` block and run the GUI main loop until all figure windows
        are closed.

        If `False` ensure that all figure windows are displayed and return
        immediately.  In this case, you are responsible for ensuring
        that the event loop is running to have responsive figures.

        Defaults to True in non-interactive mode and to False in interactive
        mode (see `.is_interactive`).

    """
    # TODO handle single figure

    # call this to ensure a backend is indeed selected
    backend = _cbm()
    managers = []
    for fig in figs:
        if fig.canvas.manager is not None:
            managers.append(fig.canvas.manager)
        else:
            managers.append(promote_figure(fig))

    if block is None:
        block = not is_interactive()

    if block and len(managers):
        if timeout == 0:
            backend.show_managers(managers=managers, block=block)
        elif len(managers):
            manager, *_ = managers
            manager.canvas.start_event_loop(timeout=timeout)


class FigureRegistry:
    """
    A registry to wrap the creation of figures and track them.

    This instance will keep a hard reference to created Figures to ensure
    that they do not get garbage collected.

    Parameters
    ----------
    block : bool, optional
        Whether to wait for all figures to be closed before returning from
        show_all.

        If `True` block and run the GUI main loop until all figure windows
        are closed.

        If `False` ensure that all figure windows are displayed and return
        immediately.  In this case, you are responsible for ensuring
        that the event loop is running to have responsive figures.

        Defaults to True in non-interactive mode and to False in interactive
        mode (see `.is_interactive`).

    timeout : float, optional
        Default time to wait for all of the Figures to be closed if blocking.

        If 0 block forever.

    """

    def __init__(self, *, block=None, timeout=0, prefix="Figure "):
        # settings stashed to set defaults on show
        self._timeout = timeout
        self._block = block
        # Settings / state to control the default figure label
        self._count = count()
        self._prefix = prefix
        # the canonical location for storing the Figures this registry owns.
        # any additional views must never include a figure not in the list but
        # may omit figures
        self.figures = []

    def _register_fig(self, fig):
        # if the user closes the figure by any other mechanism, drop our
        # reference to it.  This is important for getting a "pyplot" like user
        # experience
        fig.canvas.mpl_connect(
            "close_event",
            lambda e: self.figures.remove(fig) if fig in self.figures else None,
        )
        # hold a hard reference to the figure.
        self.figures.append(fig)
        # Make sure we give the figure a quasi-unique label.  We will never set
        # the same label twice, but will not over-ride any user label (but
        # empty string) on a Figure so if they provide duplicate labels, change
        # the labels under us, or provide a label that will be shadowed in the
        # future it will be what it is.
        fignum = next(self._count)
        if fig.get_label() == "":
            fig.set_label(f"{self._prefix}{fignum:d}")
        return fig

    @property
    def by_label(self):
        """
        Return a dictionary of the current mapping labels -> figures.

        If there are duplicate labels, newer figures will take precedence.
        """
        return {fig.get_label(): fig for fig in self.figures}

    @functools.wraps(figure)
    def figure(self, *args, **kwargs):
        fig = figure(*args, **kwargs)
        return self._register_fig(fig)

    @functools.wraps(subplots)
    def subplots(self, *args, **kwargs):
        fig, axs = subplots(*args, **kwargs)
        return self._register_fig(fig), axs

    @functools.wraps(subplot_mosaic)
    def subplot_mosaic(self, *args, **kwargs):
        fig, axd = subplot_mosaic(*args, **kwargs)
        return self._register_fig(fig), axd

    def show_all(self, *, block=None, timeout=None):
        """
        Show all of the Figures that the FigureRegistry knows about.

        Parameters
        ----------
        block : bool, optional
            Whether to wait for all figures to be closed before returning from
            show_all.

            If `True` block and run the GUI main loop until all figure windows
            are closed.

            If `False` ensure that all figure windows are displayed and return
            immediately.  In this case, you are responsible for ensuring
            that the event loop is running to have responsive figures.

            Defaults to the value set on the Registry at init

        timeout : float, optional
            time to wait for all of the Figures to be closed if blocking.

            If 0 block forever.

            Defaults to the timeout set on the Registry at init
        """
        if block is None:
            block = self._block

        if timeout is None:
            timeout = self._timeout

        show(self.figures, block=self._block, timeout=self._timeout)

    # alias to easy pyplot compatibility
    show = show_all

    def close_all(self):
        """
        Close all Figures know to this Registry.

        This will do four things:

        1. call the ``.destory()`` method on the manager
        2. clears the Figure on the canvas instance
        3. replace the canvas on each Figure with a new `~matplotlib.backend_bases.FigureCanvasBase` instance
        4. drops its hard reference to the Figure

        If the user still holds a reference to the Figure it can be revived by
        passing it to `show`.

        """
        for fig in self.figures:
            if fig.canvas.manager is not None:
                fig.canvas.manager.destroy()
            # disconnect figure from canvas
            fig.canvas.figure = None
            # disconnect canvas from figure
            _FigureCanvasBase(figure=fig)
        self.figures.clear()

    def close(self, val):
        if val != "all":
            # TODO close figures 1 at a time
            raise RuntimeError("can only close them all")
        self.close_all()


class FigureContext(FigureRegistry):
    """
    Extends FigureRegistry to be used as a context manger.

    All figures known to the Registry will be shown on exiting the context.

    Parameters
    ----------
    block : bool, optional
        Whether to wait for all figures to be closed before returning from
        show_all.

        If `True` block and run the GUI main loop until all figure windows
        are closed.

        If `False` ensure that all figure windows are displayed and return
        immediately.  In this case, you are responsible for ensuring
        that the event loop is running to have responsive figures.

        Defaults to True in non-interactive mode and to False in interactive
        mode (see `.is_interactive`).

    timeout : float, optional
        Default time to wait for all of the Figures to be closed if blocking.

        If 0 block forever.

    forgive_failure : bool, optional
        If True, block to show the figure before letting the exception
        propagate

    """

    def __init__(self, *, forgive_failure=False, **kwargs):
        super().__init__(**kwargs)
        self._forgive_failure = forgive_failure

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None and not self._forgive_failure:
            return
        show(self.figures, block=self._block, timeout=self._timeout)


# from mpl_gui import * # is a langauge miss-feature
__all__ = []
