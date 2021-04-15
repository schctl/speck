"""
Window styling utilities.

Authors:
    Sachin Cherian
"""

import json

__all__ = [
    'WindowStyle',
    'FontStyle',
    'ColorStyle',
    'SpeckStyle'
]

class WindowStyle:
    """Details about the main window."""
    def __init__(self, width, height, *args, **kwargs):
        self.width = width
        self.height = height

class FontStyle:
    """Details about fonts to be used."""
    def __init__(self, family, sizes):
        self.family = family

        self.size_big = sizes["big"]
        self.size_medium = sizes["medium"]
        self.size_small = sizes["small"]

class ColorStyle:
    """Details for colors to be used."""
    def __init__(self, fg, bg):
        self.fg = fg
        self.bg = bg

class SpeckStyle:
    """Container around all other styles."""

    def __init__(self, window, fonts, colors, *args, **kwargs):
        self.window = window
        self.fonts = fonts
        self.colors = colors

    @classmethod
    def from_file(cls, file):
        """Create an instance of ``SpeckStyle``, with details read from a file with data in json format."""
        with open(file, 'r') as f:
            data = json.load(f)

            window = WindowStyle(**data["window"])

            fonts = { i: FontStyle(**data["fonts"][i]) for i in data["fonts"] }
            colors = { i: ColorStyle(**data["colors"][i]) for i in data["colors"] }

            return cls(window, fonts, colors)
