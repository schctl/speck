Module \<`widget`\>
===================
Widget helpers for tkinter.

<sup>*class*</sup> `Widget`
----------------------------
Wrapper around Tkiner Widgets.

### `__init__(self, internal, position)`

### Attributes
- `internal`
<br>        Internal Tkinter Widget.

- `position`
<br>        Intended position of the widget.

### Methods
- `destroy(self)`
<br>        Destroy the internal tkinter widget if it exists.


<sup>*class*</sup> `WidgetManager`
----------------------------------
Keep track of Tkinter Widgets.

### `__init__()`

### Methods
 - `extend(self, widgets)`
<br>        Extend the widget list.

- `push(self, widget)`
<br>        Add a new widget to the stack. Returns the index of the widget.

- `pop(self, _id)`
<br>        Remove a widget from the lift by index.

- `clear(self)`
<br>        Clear all widgets.

- `empty(self)`
<br>        Empty the widget list.

- `render_all(self, canvas)`
<br>        Render all widgets currently in the stack onto a canvas.
