import sys
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


def test_ioff():
    with mg.ioff():
        assert not mg.is_interactive()


def test_timeout():
    fig = mg.Figure()
    mg.show([fig], block=True, timeout=1)


def test_test_context_timeout():
    with mg.FigureContext(block=True, timeout=1) as fc:
        fc.figure()
        fc.subplots()
        fc.subplot_mosaic("A\nB")
