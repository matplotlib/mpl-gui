=======
mpl-gui
=======

.. image:: https://img.shields.io/travis/tacaswell/mpl-gui.svg
        :target: https://travis-ci.org/tacaswell/mpl-gui

.. image:: https://img.shields.io/pypi/v/mpl-gui.svg
        :target: https://pypi.python.org/pypi/mpl-gui


Prototype project for splitting pyplot in half

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://tacaswell.github.io/mpl-gui.

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


Examples
--------

No pyplot usages
++++++++++++++++

If you want to be sure that this code does not secretly depend on pyplot run ::

  import sys
  sys.module['matplotlib.pyplot'] = None


which will prevent pyplot from being imported!


show
++++

The core of the API is ``show`` ::

  import mpl_gui as mg
  from mpl_gui import Figure  # shim to pass the label as a kwarg!

  fig1 = mg.Figure(label='A Label!')

  fig2 = mg.Figure()

  mg.show([fig1, fig2])


which will show both figures and block until they are closed.


blocking
++++++++

Similar to ``plt.ion`` and ``plt.ioff``, we provide ``mg.ion()`` and
``mg.ioff()`` which have identical semantics.  Thus :::

  import mpl_gui as mg
  mg.ion()

  fig = mg.Figure()

  mg.show([fig])  # will not block

  mg.ioff()

  mg.show([fig])  # will block!


As with ``plt.show``, you can explicitly control the blocking behavior of
``mg.show`` via the *block* keyword argument ::

  import mpl_gui as mg

  fig = mg.Figure(label='control blocking')

  mg.show([fig], block=False)  # will never block
  mg.show([fig], block=True)   # will always block


Figure Creation
+++++++++++++++

If you want to use the explicit Matplotlib API and also make use of the GUI integration and management, the easiest path is to start your code with one of ::

  import matplotlib.pyplot as plt
  fig1 = plt.figure()
  fig2, axs = plt.subplots(2, 2)
  fig3, axd = plt.subplot_module('AA\nBC')

  plt.show()

which gets you figures on the screen with a toolbar, but it obligatorily also
registers those figures with the pyplot global registry.  By analogy we provide ::

  import mpl_gui as mg
  fig1 = mg.figure()
  fig2, axs = mg.subplots(2, 2)
  fig3, axd = mg.subplot_module('AA\nBC')

  mg.show([fig1, fig2, fig3])


FigureContext
+++++++++++++

A very common use case is to make several figures and then show them all
together at the end.  To facilitate this we provide a context manager that
(locally) keeps track of the created figures and shows them on exit ::

  import mpl_gui as mg

  with mg.FigureContext() as fc:
     fc.subplot_mosaic('AA\nBC')
     fc.figure()
     fc.subplots(2, 2)


This will create 3 figures and block on ``__exit__``.  The blocking
behavior depends on ``mg.is_interacitve()`` (and follow the behavior of
``mg.show`` or can explicitly controlled via the *block* keyword argument.
