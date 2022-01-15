mpl gui
=======

.. module:: mpl_gui

Show
----

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.show


Interactivity
-------------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.ion
   mpl_gui.ioff
   mpl_gui.is_interactive


Figure Fabrication
------------------

Un-managed
++++++++++


.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.figure
   mpl_gui.subplots
   mpl_gui.subplot_mosaic


.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.promote_figure

Managed
+++++++


.. autoclass:: mpl_gui.FigureRegistry
   :no-undoc-members:
   :show-inheritance:


.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.FigureRegistry.figure
   mpl_gui.FigureRegistry.subplots
   mpl_gui.FigureRegistry.subplot_mosaic
   mpl_gui.FigureRegistry.by_label
   mpl_gui.FigureRegistry.show_all
   mpl_gui.FigureRegistry.close_all


.. autoclass::    mpl_gui.FigureContext
   :no-undoc-members:
   :show-inheritance:






Select the backend
------------------
.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.select_gui_toolkit
