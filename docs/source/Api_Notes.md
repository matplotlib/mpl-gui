# API design notes

## Current state

### `fig, ax = plt.subplots()  # and friends`

- To show during interactive use or in a script: `plt.show()` will show all figures that have been created by pyplot that have note been `plt.close()`d.
- `plt.show(block=False)` will show the current figure, but continue the script.
- works with `inline`
- works with ipympl

#### Pros:

- easy to show all plots.

#### Cons:

- mixed in with rest of `pyplot`
- too many figures open; must manually close the ones we don't want anymore or memory grows.  For a large jupyter notebook with cells executed many times, this can actually be substantial.

### `fig = matplotlib.figure.Figure()`

- cannot do `fig.show()`, but can do `fig.savefig()`
- does not display anything in either `inline` or `ipympl`

### Pros:

- `fig` will be garbage collected because there are no references stored in a registry

### Cons:

- no way to show the figure on a GUI backend (no promotion possible).
- ugly import.

## Proposed changes

### `mpl_gui`

- `import matplotlib.mpl_gui as mg;  fig, ax = mg.subplots()`
- Can be shown, but with new `mg.show([fig])` (though singleton fig could trivially be added).
- jupyter: works without `show` in `ipympl`; does _not_ (currently) work (at all) with `inline`.

#### Pros:

- no global state - garbage collection on dereferenced figures
- no connection to pyplot state-based interface

#### Cons:

- New import and documentation (inertia relative to pyplot)
- `mg.show()` doesn't know what figures to show, so it must be supplied a list of figures.
   - sometimes we create figures in loops, and assigning a different variable name to each figure to stop if from being dereferenced could be cumbersome.

### `mpl_gui.registry`

- `import matplotlib.mpl_gui.registry as mr; fig, ax = mr.subplots()`
- allows `mr.show()` to be exactly the same as `plt.show`.

#### Pros:

- no connection to pyplot state-based interface
- exactly same as previous pyplot interface for this type of work.

#### Cons:

- figures must be explicitly closed

### `mpl_gui.FigureContext`

This is between the two extremes, where there is no global registry, but a registry is maintained for a series of plots within a context:

```
with mg.FigureContext() as fc:
    fig, ax = fc.subplots()
    fig, ax = fc.subplot_mosaic('AA\nBC')
    fig = fc.figure
```

makes three figures and shows them in a blocking manner, and then removes the registry on completion.

### Top-level import?

The question arose as to whether these should be top level imports eg `fig, ax = mpl.subplots()`  A choice would need to be made as to whether that is the registry or non-registry version of the new interface.
