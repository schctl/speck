"""
Utility classes for easy conversions.
"""

from dataclasses import dataclass as __dc

# The use of dataclasses here
# ---------------------------
# The dataclasses module provides a decorator and
# functions for automatically generating special methods
# such as __repr__() for user-defined classes
# [docs](https://docs.python.org/3/library/dataclasses.html).

@__dc(frozen=True)
class Km:
    """Kilometer."""
    val: float

    def mi(self):
        """Equivalent miles."""
        return self.val * 0.6213

    def __repr__(self):
        return f"{self.val}"

@__dc(frozen=True)
class Cel:
    """Celsius."""
    val: float

    def fahrenheit(self):
        """Equivalent farenheit."""
        return (self.val * 1.8) + 32

    def kelvin(self):
        """Equivalent farenheit."""
        return self.val + 273.15

    def __repr__(self):
        return f"{self.val}"

@__dc(frozen=True)
class Mm:
    """Milimeters."""
    val: float

    def inches(self):
        """Equivalent inches."""
        return self.val * 0.0393

    def __repr__(self):
        return f"{self.val}"

@__dc(frozen=True)
class Mb:
    """Milibar."""
    val: float

    def inches(self):
        """Equivalent inches of Hg."""
        return self.val * 0.02952

    def __repr__(self):
        return f"{self.val}"
