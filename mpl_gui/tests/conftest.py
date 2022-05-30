from matplotlib.backend_bases import (
    _Backend,
    FigureCanvasBase,
    FigureManagerBase,
    ShowBase,
)
import mpl_gui
import sys

def pytest_configure(config):
    # config is initialized here rather than in pytest.ini so that `pytest
    # --pyargs matplotlib` (which would not find pytest.ini) works.  The only
    # entries in pytest.ini set minversion (which is checked earlier),
    # testpaths/python_files, as they are required to properly find the tests
    for key, value in [
        ("filterwarnings", "error"),
    ]:
        config.addinivalue_line(key, value)

    # make sure we do not sneakily get pyplot
    assert sys.modules.get("matplotlib.pyplot") is None
    sys.modules["matplotlib.pyplot"] = None


class TestManger(FigureManagerBase):
    _active_managers = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_info = {}

    def show(self):
        self.call_info["show"] = {}

    def destroy(self):
        self.call_info["destroy"] = {}


class TestCanvas(FigureCanvasBase):
    manager_class = TestManger

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_info = {}

    def start_event_loop(self, timeout=0):
        self.call_info["start_event_loop"] = {"timeout": timeout}


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
