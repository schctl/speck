"""
Widget helpers for tkinter.
"""

__all__ = [
    'Widget',
    'WidgetManager'
]


class Widget:
    """
    The Widget class is a utility wrapped around tkinter widgets.
    It is intended to be used with a "manager" class, and its attributes
    are kept ambiguous on purpose to the manager can use them more flexibly.
    """

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
    Basic implementation for a widget manager, to keep track of Tkinter Widgets.

    Widgets must have ``internal`` attribute which points to actual Tkinter widget object, and
    a ``position`` attribute which can either be ``int`` or ``str``. If it is a ``str``,
    it should begin with ``+``/``-``/``int``, and will be positioned relative to the last widget
    pushed onto the queue. The prefix will be ignored for the first widget in the queue.
    """

    def __init__(self):
        self._widgets = []

    def extend(self, widgets):
        """Extend the widget list."""
        self._widgets.extend(widgets)
        return [len(self._widgets) - (i + 1) for i in range(0, len(widgets), -1)]

    def push(self, widget):
        """Add a new widget to the queue. Returns the index of the widget."""
        self._widgets.append(widget)
        return len(self._widgets) - 1

    def pop(self, _id):
        """Remove a widget from the queue by index."""
        return self._widgets.pop(_id)

    # `empty` reassigns an empty list with 0 space to the queue.
    # `clear` only removes each widget, but the queue takes up
    # the same space in memory. This may be faster since
    # it won't have to be reallocated (until it takes up > `size` again).

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

    def __get_position(self, index, position_index): # position_index -> x/y -> 0/1
        """Get position of previous widget in the queue."""

        pos = self._widgets[index].position[position_index]

        if isinstance(pos, str):
            try:
                if index == 0:
                    # If we are at the end of the queue,
                    # we have to interpret position as absolute since there
                    # is nothing to position it relative to.
                    # This is a safeguard in case its provided position is a str.
                    return int(pos.lstrip('+').lstrip('-'))
                else:
                    # This will recursively get the position of the last
                    # widget, walking down the queue until we reach index 0
                    if pos[0] == '-':
                        return self.__get_position(index - 1, position_index) - \
                               int(pos.lstrip('-'))
                    elif pos[0] == '+':
                        return self.__get_position(index - 1, position_index) + \
                               int(pos.lstrip('+'))
                    else:
                        raise ValueError("Invalid format for widget position (Must be `+x`, `-x` or int).")

            except ValueError as e:
                raise ValueError from e

        elif isinstance(pos, int) or isinstance(pos, float):
            return pos

        else:
            raise TypeError("Invalid type for widget position.")

    def render_all(self, canvas):
        """Render all widgets currently in the queue onto a canvas."""

        for n, i in enumerate(self._widgets):
            x_pos = self.__get_position(n, 0)
            y_pos = self.__get_position(n, 1)

            canvas.create_window(x_pos, y_pos, anchor='nw', window=i.internal)
