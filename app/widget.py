"""
Widget helpers for tkinter.

Authors:
    Sachin Cherian
"""

__all__ = [
    'Widget',
    'WidgetManager'
]

class Widget:
    """Wrapper around Tkiner Widgets."""

    def __init__(self, internal, position):
        self._internal = internal
        self._position = position # position is ambiguous on purpose

    @property
    def internal(self):
        """Internal Tkinter Widget."""
        return self._internal

    @property
    def position(self):
        """
        Intended position of the widget relative to the
        top left corner of the root.
        """
        return self._position

    def destroy(self):
        """Destroy the internal tkinter widget if it exists."""
        if self._internal:
            self._internal.destroy()

class WidgetManager:
    """
    Keep track of Tkinter Widgets. The position of the widget can either be `int` or `str`.
    If it is a `str`, it should begin with `+`/`-`/`int`, and will be positioned relative
    to the last widget pushed onto the stack. Will be ignored for the first widget in the stack.
    """

    def __init__(self):
        self._widgets = []

    def extend(self, widgets):
        """Extend the widget list."""
        self._widgets.extend(widgets)
        return [len(self._widgets) - (i + 1) for i in range(0, len(widgets), -1)]

    def push(self, widget):
        """Add a new widget to the stack. Returns the index of the widget."""
        self._widgets.append(widget)
        return len(self._widgets) - 1

    def pop(self, _id):
        """Remove a widget from the lift by index."""
        return self._widgets.pop(_id)

    def clear(self):
        """Clear all widgets."""
        for i in self._widgets:
            i.destroy()
        self._widgets.clear()

    def empty(self):
        """Empty the widget list."""
        for i in self._widgets:
            i.destroy()
        self._widgets = []

    def __get_position_from_prev(self, index, position_index): # position_index -> x/y -> 0/1
        """Get position of previous widget in the stack."""
        pos = self._widgets[index].position[position_index]

        # TODO: more descriptive errors.

        if isinstance(pos, str):
            try:
                if index == 0:
                    return int(pos.lstrip('+').lstrip('-'))
                else:
                    if pos[0] == '-':
                        return self.__get_position_from_prev(index - 1, position_index) - \
                               int(pos.lstrip('-'))
                    elif pos[0] == '+':
                        return self.__get_position_from_prev(index - 1, position_index) + \
                               int(pos.lstrip('+'))
                    else:
                        raise ValueError("Invalid format for widget position (Must be `+x`, `-x` or int).")

            except ValueError as e:
                raise ValueError from e

        elif isinstance(pos, int):
            return pos

        else:
            raise TypeError("Invalid type for widget position.")

    def render_all(self, canvas):
        """Render all widgets currently in the stack onto a canvas."""
        for n, i in enumerate(self._widgets):
            x_pos = self.__get_position_from_prev(n, 0)
            y_pos = self.__get_position_from_prev(n, 1)

            canvas.create_window(x_pos, y_pos, anchor='nw', window=i.internal)
