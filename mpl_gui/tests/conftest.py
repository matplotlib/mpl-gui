from matplotlib.backend_bases import _Backend, FigureCanvasBase, FigureManagerBase
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_info = {}

    def show(self):
        self.call_info["show"] = {}


class TestingBackend(_Backend):
    FigureCanvas = TestCanvas
    FigureManager = TestManger


mpl_gui.switch_backend(TestingBackend)
