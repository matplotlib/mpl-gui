.. Packaging Scientific Python documentation master file, created by
   sphinx-quickstart on Thu Jun 28 12:35:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================
 mpl-gui Documentation
=======================

.. toctree::
   :maxdepth: 2

   api
   release_history
   min_versions


Motivation
==========

This project is a prototype space for overhauling the GUI event loop management
tools that Matplotlib provides in pyplot.

The pyplot module current serves two critical, but unrelated functions:

1. provide a state-full implicit API that rhymes / was inspired by MATLAB
2. provide the management of interaction between Matplotlib and the GUI event
   loop, including keeping Figures alive

While it can be very convenient when working at the prompt, the state-full API
can lead to brittle code that depends on the global state in confusing ways,
particularly when used in library code.  On the other hand,
``matplotlib.pyplot`` does a very good job of hiding from the user the fact
that they are developing a GUI application and handling, along with IPython,
many of the details involved in running a GUI application in parallel with
Python.


Examples
========

.. highlight:: python


If you want to be sure that this code does not secretly depend on pyplot run ::

  import sys
  sys.modules['matplotlib.pyplot'] = None


which will prevent pyplot from being imported!


showing
-------

The core of the API is `~.show` ::

  import mpl_gui as mg
  from matplotlib.figure import Figure

  fig1 = Figure(label='A Label!')

  fig2 = Figure()

  mg.show([fig1, fig2])


which will show both figures and block until they are closed.  As part of the
"showing" process, the correct GUI objects will be created, put on the
screen, and the event loop for the host GUI framework is run.


blocking (or not)
+++++++++++++++++

Similar to `plt.ion<matplotlib.pyplot.ion>` and
`plt.ioff<matplotlib.pyplot.ioff>`, we provide `mg.ion()<mpl_gui.ion>` and
`mg.ioff()<mpl_gui.ioff>` which have identical semantics.  Thus  ::

  import mpl_gui as mg
  from matplotlib.figure import Figure

  mg.ion()
  print(mg.is_interactive())
  fig = Figure()

  mg.show([fig])  # will not block

  mg.ioff()
  print(mg.is_interactive())
  mg.show([fig])  # will block!


As with `plt.show<matplotlib.pyplot.show>`, you can explicitly control the
blocking behavior of `mg.show<.show>` via the *block* keyword argument ::

  import mpl_gui as mg
  from matplotlib.figure import Figure

  fig = Figure(label='control blocking')

  mg.show([fig], block=False)  # will never block
  mg.show([fig], block=True)   # will always block


The interactive state is shared Matplotlib and can also be controlled with
`matplotlib.interactive` and queried via `matplotlib.is_interactive`.


Figure and Axes Creation
------------------------

In analogy with `matplotlib.pyplot` we also provide `~mpl_gui.figure`,
`~mpl_gui.subplots` and `~mpl_gui.subplot_mosaic` ::

  import mpl_gui as mg
  fig1 = mg.figure()
  fig2, axs = mg.subplots(2, 2)
  fig3, axd = mg.subplot_mosaic('AA\nBC')

  mg.show([fig1, fig2, fig3])

If `mpl_gui` is in "interactive mode", `mpl_gui.figure`, `mpl_gui.subplots` and
`mpl_gui.subplot_mosaic` will automatically put the new Figure in a window on
the screen (but not run the event loop).



FigureRegistry
--------------

In the above examples it is the responsibility of the user to keep track of the
`~matplotlib.figure.Figure` instances that are created.  If the user does not keep a hard
reference to the ``fig`` object, either directly or indirectly through its
children, then it will be garbage collected like any other Python object.
While this can be advantageous in some cases (such as scripts or functions that
create many transient figures).  It loses the convenience of
`matplotlib.pyplot` keeping track of the instances for you.  To this end we
also have provided `.FigureRegistry` ::

  import mpl_gui as mg

  fr = mg.FigureRegistry()

  fr.figure()
  fr.subplots(2, 2)
  fr.subplot_mosaic('AA\nBC')

  fr.show_all()     # will show all three figures
  fr.show()         # alias for pyplot compatibility

  fr.close_all()    # will close all three figures
  fr.close('all')   # alias for pyplot compatibility

Thus, if you are only using this restricted set of the pyplot API then you can change ::

  import matplotlib.pyplot as plt

to ::

  import mpl_gui as mg
  plt = mg.FigureRegistry()

and have a (mostly) drop-in replacement.

Additionally, there is a  `.FigureRegistry.by_label` accessory that returns
a dictionary mapping the Figures' labels to each Figure ::

  import mpl_gui as mg

  fr = mg.FigureRegistry()

  figA = fr.figure(label='A')
  figB = fr.subplots(2, 2, label='B')

  fr.by_label['A'] is figA
  fr.by_label['B'] is figB

FigureContext
-------------

A very common use case is to make several figures and then show them all
together at the end.  To facilitate this we provide a sub-class of
`.FigureRegistry` that can be used as a context manager that (locally) keeps
track of the created figures and shows them on exit ::

  import mpl_gui as mg

  with mg.FigureContext() as fc:
      fc.subplot_mosaic('AA\nBC')
      fc.figure()
      fc.subplots(2, 2)


This will create 3 figures and block on ``__exit__``.  The blocking
behavior depends on ``mg.is_interacitve()`` (and follow the behavior of
``mg.show`` or can explicitly controlled via the *block* keyword argument).


Selecting the GUI toolkit
-------------------------

`mpl_gui` makes use of `Matplotlib backends
<https://matplotlib.org/stable/users/explain/backends.html>`_ for actually
providing the GUI bindings.  Analagous to `matplotlib.use` and
`matplotlib.pyplot.switch_backend` `mpl_gui` provides
`mpl_gui.select_gui_toolkit` to select which GUI toolkit is used.
`~mpl_gui.select_gui_toolkit` has the same fall-back behavior as
`~matplotlib.pyplot` and stores its state in :rc:`backend`.  `mpl_gui` will
consistently co-exist with `matplotlib.pyplot` managed Figures in the same
process.
