from matplotlib.backends.backend_tkagg import _BackendTkAgg


@_BackendTkAgg.export
class _PatchedBackendTkAgg(_BackendTkAgg):
    @staticmethod
    def get_active_managers():
        raise RuntimeError("This method should never actually be called")

    @classmethod
    def mainloop(cls):
        managers = cls.get_active_managers()
        if managers:
            first_manager = managers[0]
            manager_class = type(first_manager)
            if manager_class._owns_mainloop:
                return
            manager_class._owns_mainloop = True
            try:
                first_manager.window.mainloop()
            finally:
                manager_class._owns_mainloop = False


Backend = _PatchedBackendTkAgg
