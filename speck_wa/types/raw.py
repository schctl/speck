"""
Utility classes for easy convertions.
"""

from dataclasses import dataclass as __dc

# The use of dataclasses here
# ---------------------------
# The dataclasses module provides a decorator and functions for automatically generating special methods
# such as __repr__() for user-defined classes - [docs](https://docs.python.org/3/library/dataclasses.html).

@__dc(frozen=True)
class Km:
    val: float

    def mi(self):
        return self.val * 0.6213

    def __repr__(self):
        return f"{self.val}"

@__dc(frozen=True)
class Cel:
    val: float

    def fahrenheit(self):
        return (self.val * 1.8) + 32

    def __repr__(self):
        return f"{self.val}"

@__dc(frozen=True)
class Mm:
    val: float

    def inches(self):
        return self.val * 0.0393

    def __repr__(self):
        return f"{self.val}"

@__dc(frozen=True)
class Mb:
    val: float

    def inches(self):
        return self.val * 0.02952

    def __repr__(self):
        return f"{self.val}"
