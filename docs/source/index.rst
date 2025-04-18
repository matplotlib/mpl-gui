.. Packaging Scientific Python documentation master file, created by
   sphinx-quickstart on Thu Jun 28 12:35:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================
 mpl-gui Documentation
=======================
.. highlight:: python

.. toctree::
   :maxdepth: 1

   api
   release_history
   min_versions
   Api_Notes


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
`matplotlib.pyplot` does a very good job of hiding from the user the fact
that they are developing a GUI application and handling, along with IPython,
many of the details involved in running a GUI application in parallel with
Python.


If you want to be sure that this code does not secretly depend on pyplot run ::

  import sys
  sys.modules['matplotlib.pyplot'] = None


which will prevent pyplot from being imported!



Selecting the GUI toolkit
=========================

`mpl_gui` makes use of `Matplotlib backends
<https://matplotlib.org/stable/users/explain/backends.html>`_ for actually
providing the GUI bindings.  Analagous to `matplotlib.use` and
`matplotlib.pyplot.switch_backend` `mpl_gui` provides
`mpl_gui.select_gui_toolkit` to select which GUI toolkit is used.
`~mpl_gui.select_gui_toolkit` has the same fall-back behavior as
`~matplotlib.pyplot` and stores its state in :rc:`backend`.

`mpl_gui` will
consistently co-exist with `matplotlib.pyplot` managed Figures in the same
process.



User Managed Figures
====================

There are cases where having such a registry may be too much implicit state.
For such cases the underlying tools that `.FigureRegistry` are built on are
explicitly available ::

  import mpl_gui as mg
  from matplotlib.figure import Figure

  fig1 = Figure(label='A Label!')

  fig2 = Figure()

  mg.display(fig1, fig2)


which will show both figures and block until they are closed.  As part of the
"showing" process, the correct GUI objects will be created, put on the
screen, and the event loop for the host GUI framework is run.

Similar to `plt.ion<matplotlib.pyplot.ion>` and
`plt.ioff<matplotlib.pyplot.ioff>`, we provide `mg.ion()<mpl_gui.ion>` and
`mg.ioff()<mpl_gui.ioff>` which have identical semantics.  Thus ::

  import mpl_gui as mg
  from matplotlib.figure import Figure

  mg.ion()
  print(mg.is_interactive())
  fig = Figure()

  mg.display([fig])  # will not block

  mg.ioff()
  print(mg.is_interactive())
  mg.display(fig)  # will block!


As with `plt.show<matplotlib.pyplot.show>`, you can explicitly control the
blocking behavior of `mg.display<mpl_gui.display>` via the *block* keyword argument ::

  import mpl_gui as mg
  from matplotlib.figure import Figure

  fig = Figure(label='control blocking')

  mg.display(fig, block=False)  # will never block
  mg.display(fig, block=True)   # will always block


The interactive state is shared Matplotlib and can also be controlled with
`matplotlib.interactive` and queried via `matplotlib.is_interactive`.



Locally Managed Figures
=======================

To avoid the issues with global state the objects you can create a local `.FigureRegistry`.
It keeps much of the convenience of the ``pyplot`` API but without the risk of global state ::

  import mpl_gui as mg

  fr = mg.FigureRegistry()

  fr.figure()
  fr.subplots(2, 2)
  fr.subplot_mosaic('AA\nBC')

  fr.show_all()     # will show all three figures
  fr.show()         # alias for pyplot compatibility

  fr.close_all()    # will close all three figures
  fr.close('all')   # alias for pyplot compatibility


Additionally, there are the  `.FigureRegistry.by_label`, `.FigureRegistry.by_number`,
`.FigureRegistry.figures` accessors that returns a dictionary mapping the
Figures' labels to each Figure, the figures number to Figure, and a tuple of known Figures::

  import mpl_gui as mg

  fr = mg.FigureRegistry()

  figA = fr.figure(label='A')
  figB, axs = fr.subplots(2, 2, label='B')

  fr.by_label['A'] is figA
  fr.by_label['B'] is figB

  fr.by_number[0] is figA
  fr.by_number[1] is figB

  fr.figures == (figA, figB)

  fr.show()

The `.FigureRegistry` is local state so that if the user drops all references
to it it will be eligible for garbage collection.  If there are no other
references to the ``Figure`` objects it is likely that they may be closed when
the garbage collector runs!


A very common use case is to make several figures and then show them all
together at the end.  To facilitate this we provide a `.FigureContext` that is
a `.FigureRegistry` that can be used as a context manager that (locally) keeps
track of the created figures and shows them on exit ::

  import mpl_gui as mg

  with mg.FigureContext(block=None) as fc:
      fc.subplot_mosaic('AA\nBC')
      fc.figure()
      fc.subplots(2, 2)


This will create 3 figures and block on ``__exit__``.  The blocking
behavior depends on `~mpl_gui.is_interactive()` (and follow the behavior of
`.display` and `.FigureRegistry.show` can explicitly controlled via the *block* keyword argument).

The `.global_figures` module is implemented by having a singleton `.FigureRegistry`
at the module level.




Globally Managed Figures
========================


The `mpl_gui.global_figures` module provides a direct analogy to the
`matplotlib.pyplot` behavior of having a global registry of figures.  Thus, any
figures created via the functions in `.global_figures` will remain alive until they
have been cleared from the registry (and the user has dropped all other
references).  While it can be convenient, it carries with it the risk inherent
in any use of global state.

The `matplotlib.pyplot` API related to figure creation, showing, and closing is a drop-in replacement:

::

   import mpl_gui.global_figures as gfigs

   fig = gfigs.figure()
   fig, ax = gfigs.subplots()
   fig, axd = gfigs.subplot_mosaic('AA\nCD')

   gfigs.show(block=True)                # blocks until all figures are closed
   gfigs.show(block=True, timeout=1000)  # blocks for up to 1s or all figures are closed
   gfigs.show(block=False)               # does not block
   gfigs.show()                          # depends on if in "interacitve mode"

   gfigs.ion()                           # turn on interactive mode
   gfigs.ioff()                          # turn off interactive mode
   gfigs.is_interactive()                # query interactive state

   gfigs.close('all')                    # close all open figures
   gfigs.close(fig)                      # close a particular figure
