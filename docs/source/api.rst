mpl gui API Reference
=====================

.. automodule:: mpl_gui
   :no-undoc-members:



Select the backend
------------------
.. autosummary::
   :toctree: _as_gen


   select_gui_toolkit


Interactivity
-------------

.. autosummary::
   :toctree: _as_gen


   ion
   ioff
   is_interactive


Unmanaged Figures
-----------------

Figure Creation
+++++++++++++++

These are not strictly necessary as they are only thin wrappers around creating
a `matplotlib.figure.Figure` instance and creating children in one line.

.. autosummary::
   :toctree: _as_gen



   figure
   subplots
   subplot_mosaic



Display
+++++++

.. autosummary::
   :toctree: _as_gen



   display
   demote_figure



Locally Managed Figures
-----------------------


.. autoclass:: FigureRegistry
   :no-undoc-members:
   :show-inheritance:


.. autoclass::    FigureContext
   :no-undoc-members:
   :show-inheritance:

Create Figures and Axes
+++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen


   FigureRegistry.figure
   FigureRegistry.subplots
   FigureRegistry.subplot_mosaic


Access managed figures
++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen


   FigureRegistry.by_label
   FigureRegistry.by_number
   FigureRegistry.figures



Show and close managed Figures
++++++++++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen


   FigureRegistry.show_all
   FigureRegistry.close_all
   FigureRegistry.show
   FigureRegistry.close




Globally managed
----------------


.. automodule:: mpl_gui.global_figures
   :no-undoc-members:



Create Figures and Axes
+++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen


   figure
   subplots
   subplot_mosaic


Access managed figures
++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen


   by_label


Show and close managed Figures
++++++++++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen




   show
   show_all
   close_all
   close


Interactivity
+++++++++++++

.. autosummary::
   :toctree: _as_gen



   ion
   ioff
   is_interactive
