import argparse
import sys

import matplotlib as mpl
import mpl_gui as mg
from matplotlib.figure import Figure

# ensure no pyplot!
assert sys.modules.get("matplotlib.pyplot", None) is None
sys.modules["matplotlib.pyplot"] = None

parser = argparse.ArgumentParser(
    description="User Acceptance Tests for mpl-gui.",
    epilog=(
        "This script runs through several scenarios and prints out prompts explaining the expected behavior.  "
        "The figures will need to be closed to continue the script.  "
    ),
)
parser.add_argument(
    "backend",
    type=str,
    help="The backend to use.  Can be anything that `mpl.use` accepts",
)

args = parser.parse_args()
target = args.backend


# this is how to force the right Qt binding
if target.lower().startswith("qt5"):
    import PyQt5.QtWidgets  # noqa
elif target.lower().startswith("qt"):
    import PyQt6.QtWidgets  # noqa

mpl.use(target, force=True)

fig1 = Figure(label="A Label!")

fig2 = Figure()

print(
    """
You should see two figures with window titles of

 - "A Label!"
 - "Figure 0"

both should be empty and the process should block until both
are closed (the keybinding 'q' should work).
"""
)
mg.show([fig1, fig2])

mg.ion()
fig = Figure()
print(f"Interactive mode is on: {mg.is_interactive()}")
mg.show([fig])  # will not block
print("A (implicitly) non-blocking show was just called.")
mg.ioff()
print(mg.is_interactive())
print(f"Interactive mode is on: {mg.is_interactive()}")
print(
    """
You should see one open figure with the title

- Figure 2

and the process should again block until it is closed.
"""
)

mg.show([fig])  # will block!

fig = Figure(label="control blocking")

mg.show([fig], block=False)  # will never block
print("A (implicitly) non-blocking show was just called.")
print(
    """
You should see one open figure with the title

- control blocking

and the process should again block until it is closed.
"""
)
mg.show([fig], block=True)  # will always block


fig1 = mg.figure()
fig2, axs = mg.subplots(2, 2)
fig3, axd = mg.subplot_mosaic("AA\nBC")

print(
    """
You should see three open figure with the titles

- Figure 4
- Figure 5
- Figure 6

and the process should again block until it is closed.  One will
be empty, one will have a 2x2 grid, One will have `AA;BC` layout.
"""
)

mg.show([fig1, fig2, fig3])


fr = mg.FigureRegistry()

fr.figure()
fr.subplots(2, 2)
fr.subplot_mosaic("AA\nBC")

print(
    """
You should see three open figure with the titles

- Figure 0
- Figure 1
- Figure 2

and the process should again block until it is closed.  One will
be empty, one will have a 2x2 grid, One will have `AA;BC` layout.
"""
)

fr.show_all()  # will show all three figures
# fr.show()  # alias for pyplot compatibility

# fr.close_all()  # will close all three figures
# fr.close("all")  # alias for pyplot compatibility


plt = mg.FigureRegistry()


with mg.FigureContext() as fc:
    fc.subplot_mosaic("AA\nBC")
    fc.figure()
    fc.subplots(2, 2)

    print(
        """
You should see three open figure with the titles

- Figure 0
- Figure 1
- Figure 2

and the process should again block until it is closed.  One will
be empty, one will have a 2x2 grid, One will have `AA;BC` layout.
"""
    )
