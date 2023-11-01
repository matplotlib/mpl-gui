mpl gui API Reference
=====================

.. automodule:: mpl_gui
   :no-undoc-members:



Select the backend
------------------
.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.select_gui_toolkit


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
   :nosignatures:

   mpl_gui.FigureRegistry.figure
   mpl_gui.FigureRegistry.subplots
   mpl_gui.FigureRegistry.subplot_mosaic


Access managed figures
++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.FigureRegistry.by_label
   mpl_gui.FigureRegistry.by_number
   mpl_gui.FigureRegistry.figures



Show and close managed Figures
++++++++++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.FigureRegistry.show_all
   mpl_gui.FigureRegistry.close_all
   mpl_gui.FigureRegistry.show
   mpl_gui.FigureRegistry.close




Globally managed
----------------


.. automodule:: mpl_gui.registry
   :no-undoc-members:



Create Figures and Axes
+++++++++++++++++++++++

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.registry.figure
   mpl_gui.registry.subplots
   mpl_gui.registry.subplot_mosaic


Access managed figures
++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   mpl_gui.registry.by_label


Show and close managed Figures
++++++++++++++++++++++++++++++


.. autosummary::
   :toctree: _as_gen
   :nosignatures:



   mpl_gui.registry.show
   mpl_gui.registry.show_all
   mpl_gui.registry.close_all
   mpl_gui.registry.close


Interactivity
+++++++++++++

.. autosummary::
   :toctree: _as_gen
   :nosignatures:


   mpl_gui.registry.ion
   mpl_gui.registry.ioff
   mpl_gui.registry.is_interactive
