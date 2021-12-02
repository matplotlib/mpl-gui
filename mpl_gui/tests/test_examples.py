import sys

import pytest

from matplotlib.backend_bases import FigureCanvasBase

import mpl_gui as mg



def test_no_pyplot():

    assert sys.modules.get("matplotlib.pyplot", None) is None


def test_promotion():
    fig = mg.Figure(label="test")
    assert fig.canvas.manager is None
    mg.show([fig], block=False)
    assert fig.canvas.manager is not None


def test_smoke_test_creation():
    mg.figure()
    mg.subplots()
    mg.subplot_mosaic("A\nB")


def test_smoke_test_context():
    with mg.FigureContext(block=False) as fc:
        fc.figure()
        fc.subplots()
        fc.subplot_mosaic("A\nB")


def test_ion():
    with mg.ion():
        assert mg.is_interactive()
        fig, ax = mg.subplots()
        (ln,) = ax.plot(range(5))
        ln.set_color("k")
        mg.show([fig], timeout=1)
    assert "start_event_loop" not in fig.canvas.call_info


def test_ioff():
    with mg.ioff():
        assert not mg.is_interactive()


def test_timeout():
    fig = mg.Figure()
    mg.show([fig], block=True, timeout=1)
    assert "start_event_loop" in fig.canvas.call_info


def test_test_context_timeout():
    with mg.FigureContext(block=True, timeout=1) as fc:
        fig = fc.figure()
        fc.subplots()
        fc.subplot_mosaic("A\nB")
    assert "start_event_loop" in fig.canvas.call_info
    assert fig.canvas.call_info["start_event_loop"]["timeout"] == 1


@pytest.mark.parametrize("forgiving", [True, False])
def test_context_exceptions(forgiving):
    class TestException(Exception):
        ...

    with pytest.raises(TestException):
        with mg.FigureContext(block=True, forgive_failure=forgiving, timeout=1) as fc:
            fig = fc.figure()
            raise TestException

    if forgiving:
        assert "start_event_loop" in fig.canvas.call_info
    else:

        assert isinstance(fig.canvas, FigureCanvasBase)

def test_close_all():
    fr = mg.FigureRegistry(block=False)
    fig = fr.figure()
    assert fig in fr.figures
    assert isinstance(fig.canvas, FigureCanvasBase)
    old_canvas = fig.canvas
    fr.show_all()
    assert fig.canvas is not old_canvas
    new_canvas = fig.canvas
    fr.close_all()
    assert len(fr.figures) == 0
    assert 'destroy' in new_canvas.manager.call_info
    assert fig.canvas is not new_canvas
    assert new_canvas.figure is None

    # test revive
    old_canvas = fig.canvas
    mg.show([fig])
    assert fig.canvas is not old_canvas
