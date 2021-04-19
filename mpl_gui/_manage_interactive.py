from matplotlib import is_interactive, interactive as _interactive


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
