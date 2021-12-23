import importlib
import sys
import logging

from matplotlib import cbook, rcsetup
from matplotlib import rcParamsOrig, rcParams, rcParamsDefault

_backend_mod = None

_log = logging.getLogger(__name__)


def current_backend_module():
    """
    Get the currently active backend module
    """
    return _backend_mod


def switch_backend(newbackend=None):
    """
    Close all open figures and set the Matplotlib backend.

    The argument is case-insensitive.  Switching to an interactive backend is
    possible only if no event loop for another interactive backend has started.
    Switching to and from non-interactive backends is always possible.

    Parameters
    ----------
    newbackend : Union[str, _Backend]
        The name of the backend to use or a _Backend class to use.

    Returns
    -------
    _Backend
       The backend selected.
    """
    global _backend_mod

    # work-around the sentinel resolution in Matplotlib 😱
    if newbackend is None:
        newbackend = dict.__getitem__(rcParams, "backend")
    # make sure the init is pulled up so we can assign to it later
    import matplotlib.backends

    if newbackend is rcsetup._auto_backend_sentinel:
        current_framework = cbook._get_running_interactive_framework()
        mapping = {
            "qt": "qtagg",
            "gtk3": "gtk3agg",
            'gtk4': 'gtk4agg',
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
                return switch_backend(candidate)
            except ImportError:
                continue

        else:
            # Switching to Agg should always succeed; if it doesn't, let the
            # exception propagate out.
            return switch_backend("agg")

    if isinstance(newbackend, str):
        # Backends are implemented as modules, but "inherit" default method
        # implementations from backend_bases._Backend.  This is achieved by
        # creating a "class" that inherits from backend_bases._Backend and whose
        # body is filled with the module's globals.

        backend_name = cbook._backend_module_name(newbackend)

        class backend_mod(matplotlib.backend_bases._Backend):
            locals().update(vars(importlib.import_module(backend_name)))

        rc_params_string = newbackend

    else:
        backend_mod = newbackend
        rc_params_string = f"module://_backend_mod_{id(backend_mod)}"
        sys.modules[rc_params_string] = backend_mod

    required_framework = getattr(
        backend_mod.FigureCanvas, "required_interactive_framework", None
    )
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

    rcParams["backend"] = rcParamsDefault["backend"] = rc_params_string
    _backend_mod = backend_mod

    # is IPython imported?
    mod_ipython = sys.modules.get("IPython")
    if mod_ipython:
        # if so are we in an IPython session
        ip = mod_ipython.get_ipython()
        if ip:
            ip.enable_gui(required_framework)
    return _backend_mod
