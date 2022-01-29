from matplotlib.backend_bases import (
    _Backend,
    FigureCanvasBase,
    FigureManagerBase,
    ShowBase,
)
import mpl_gui
import sys


# make sure we do not sneakily get pyplot
sys.modules["matplotlib.pyplot"] = None


class TestCanvas(FigureCanvasBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_info = {}

    def start_event_loop(self, timeout=0):
        self.call_info["start_event_loop"] = {"timeout": timeout}


class TestManger(FigureManagerBase):
    _active_managers = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_info = {}

    def show(self):
        self.call_info["show"] = {}

    def destroy(self):
        self.call_info["destroy"] = {}


class TestShow(ShowBase):
    def mainloop(self):
        ...


class TestingBackend(_Backend):
    FigureCanvas = TestCanvas
    FigureManager = TestManger
    Show = TestShow

    @classmethod
    def mainloop(cls):
        ...

    @classmethod
    def show_managers(cls, *, managers, block):
        for m in managers:
            m.show()


mpl_gui.select_gui_toolkit(TestingBackend)
