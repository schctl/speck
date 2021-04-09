"""
Utility classes for easy convertions.
"""

class Base:
    """Abstract class for basic unit conversions."""
    def __init__(self, val):
        self.val = val

    def __call__(self):
        return self.val

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)


class Km(Base):
    def __init__(self, val):
        super().__init__(val)

    def mi(self):
        return self.val * 0.6213712

class Kph(Base):
    def __init__(self, val):
        super().__init__(val)

    def mph(self):
        return self.val * 0.6213712

class Cel(Base):
    def __init__(self, val):
        super().__init__(val)

    def fahrenheit(self):
        return (self.val * 1.8) + 32

class Mm(Base):
    def __init__(self, val):
        super().__init__(val)

    def inches(self):
        return self.val * 0.03937008

class Mb(Base):
    def __init__(self, val):
        super().__init__(val)

    def inches(self):
        return self.val * 0.029529983071445
