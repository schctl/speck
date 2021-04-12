import tkinter as tk

class Widget:
    """Wrapper around Tkiner Widgets."""

    def __init__(self, internal, position):
        self._internal = internal
        self._position = position # position is ambiguous on purpose

    @property
    def internal(self):
        return self._internal

    @property
    def position(self):
        return self._position

    def destroy(self):
        if self._internal:
            self._internal.destroy()

class WidgetManager:
    """Keep track of Tkinter Widgets."""

    def __init__(self):
        self._widgets = []

    def extend(self, widgets):
        self._widgets.extend(widgets)
        return [len(self._widgets) - (i + 1) for i in range(0, len(widgets), -1)]

    def push(self, widget):
        self._widgets.append(widget)
        return len(self._widgets) - 1

    def pop(self, _id):
        return self._widgets.pop(_id)

    def clear(self):
        for i in self._widgets:
            i.destroy()
        self._widgets.clear()

    def empty(self):
        for i in self._widgets:
            i.destroy()
        self._widgets = []

    def __get_position_from_prev(self, index, position_index): # position_index -> x/y -> 0/1
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
                raise ValueError(f"Invalid format for widget position (Must be `+x`, `-x` or int). [{e}]")

        elif isinstance(pos, int):
            return pos

        else:
            raise TypeError("Invalid type for widget position.")

    def render_all(self, canvas):
        for n, i in enumerate(self._widgets):
            x_pos = self.__get_position_from_prev(n, 0)
            y_pos = self.__get_position_from_prev(n, 1)

            canvas.create_window(x_pos, y_pos, anchor='nw', window=i.internal)
