"""
Prototype project for new Matplotlib GUI management.

The pyplot module current serves two critical, but unrelated functions:

1. provide a state-ful implicit API that rhymes / was inspired by MATLAB
2. provide the management of interaction between Matplotlib and the GUI event
   loop

This project is prototype for separating the second function from the first.
This will enable users to both only use the explicit API (nee OO interface) and
to have smooth integration with the GUI event loop as with pyplot.

"""

import logging


from matplotlib import is_interactive
from ._figure import Figure  # noqa: F401

from ._manage_interactive import ion, ioff  # noqa: F401
from ._manage_backend import switch_backend, current_backend_module
from ._creation import promote_figure
from ._creation import figure  # noqa: F401
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions


_log = logging.getLogger(__name__)


def show(figs, *, block=None, timeout=0):
    """
    Show the figures and maybe block.


    """
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
        # TODO make timeout work!
        current_backend_module().Show().mainloop()


# set up the backend!
# use getitem to escape our key magic
switch_backend()
