=======
mpl-gui
=======

.. image:: https://img.shields.io/pypi/v/mpl-gui.svg
        :target: https://pypi.python.org/pypi/mpl-gui


Prototype project for splitting pyplot in half

* Free software: 3-clause BSD license
* Documentation: https://tacaswell.github.io/mpl-gui.

Motivation
----------

This project is a prototype space for overhauling the GUI event loop management
tools that Matplotlib provides in pyplot.

The pyplot module current serves two critical, but unrelated functions:

1. provide a state-full implicit API that rhymes / was inspired by MATLAB
2. provide the management of interaction between Matplotlib and the GUI event
   loop

While it can be very convenient when working at the prompt, the state-full API
can lead to brittle code that depends on the global state in confusing ways,
particularly when used in library code.  On the other hand,
``matplotlib.pyplot`` does a very good job of hiding from the user the fact
that they are developing a GUI application and handling, along with IPython,
many of the details involved in running a GUI application in parallel with
Python.
