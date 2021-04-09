"""
Styling utilities for speck.

Authors:
    2021 Sachin Cherian
"""

import json

class WindowStyle:
    def __init__(self, width, height, *args, **kwargs):
        self.width = width
        self.height = height

class FontStyle:
    def __init__(self, family, sizes):
        self.family = family
        
        self.size_big = sizes["big"]
        self.size_medium = sizes["medium"]
        self.size_small = sizes["small"]

class ColorStyle:
    def __init__(self, fg, bg):
        self.fg = fg
        self.bg = bg

class SpeckStyle:
    def __init__(self, window, fonts, colors, *args, **kwargs):
        self.window = window
        self.fonts = fonts
        self.colors = colors

    @classmethod
    def from_file(cls, file):
        with open(file, 'r') as f:
            data = json.load(f)

        window = WindowStyle(**data["window"])

        fonts = {}
        
        for i in data["fonts"]:
            fonts[i] = FontStyle(**data["fonts"][i])

        colors = {}
        
        for i in data["colors"]:
            colors[i] = ColorStyle(**data["colors"][i])

        return cls(window, fonts, colors)
