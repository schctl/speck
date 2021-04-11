import tkinter as tk

class Widget:
    def __init__(self, internal, position):
        self._internal = internal
        self._position = position

    @property
    def internal(self):
        return self._internal

    @property
    def position(self):
        return self._position

class WidgetManager:
    def __init__(self):
        self._widgets = []

    def push(self, widget):
        self._widgets.append(widget)
        return len(self._widgets) - 1

    def remove(self, _id):
        self._widgets.pop(_id)

    def render_all(self, canvas):
        for i in self._widgets:
            canvas.create_window(i.position[0], i.position[1], anchor='nw', window=i)
