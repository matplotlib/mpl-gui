mpl gui API Reference
=====================

.. automodule:: mpl_gui
   :no-undoc-members:



Select the backend
------------------
.. autosummary::
   :toctree: _as_gen


   mpl_gui.select_gui_toolkit


Interactivity
-------------

.. autosummary::
   :toctree: _as_gen


   mpl_gui.ion
   mpl_gui.ioff
   mpl_gui.is_interactive


Unmanaged Figures
-----------------

Figure Creation
+++++++++++++++

These are not strictly necessary as they are only thin wrappers around creating
a `matplotlib.figure.Figure` instance and creating children in one line.

.. autosummary::
   :toctree: _as_gen



   mpl_gui.figure
   mpl_gui.subplots
   mpl_gui.subplot_mosaic



Display
+++++++

.. autosummary::
   :toctree: _as_gen



   mpl_gui.display
   mpl_gui.demote_figure



Locally Managed Figures
-----------------------


.. autoclass:: mpl_gui.FigureRegistry
   :no-undoc-members:
   :show-inheritance:


.. autoclass::    mpl_gui.FigureContext
   :no-undoc-members:
   :show-inheritance:

Create Figures and Axes
+++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen


   mpl_gui.FigureRegistry.figure
   mpl_gui.FigureRegistry.subplots
   mpl_gui.FigureRegistry.subplot_mosaic


Access managed figures
++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen


   mpl_gui.FigureRegistry.by_label
   mpl_gui.FigureRegistry.by_number
   mpl_gui.FigureRegistry.figures



Show and close managed Figures
++++++++++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen


   mpl_gui.FigureRegistry.show_all
   mpl_gui.FigureRegistry.close_all
   mpl_gui.FigureRegistry.show
   mpl_gui.FigureRegistry.close




Globally managed
----------------


.. automodule:: mpl_gui.global_figures
   :no-undoc-members:



Create Figures and Axes
+++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen


   mpl_gui.global_figures.figure
   mpl_gui.global_figures.subplots
   mpl_gui.global_figures.subplot_mosaic


Access managed figures
++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen


   mpl_gui.global_figures.by_label


Show and close managed Figures
++++++++++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen




   mpl_gui.global_figures.show
   mpl_gui.global_figures.show_all
   mpl_gui.global_figures.close_all
   mpl_gui.global_figures.close


Interactivity
+++++++++++++

.. autosummary::
   :toctree: _as_gen



   mpl_gui.global_figures.ion
   mpl_gui.global_figures.ioff
   mpl_gui.global_figures.is_interactive
