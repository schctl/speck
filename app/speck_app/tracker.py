"""
Tracker class.

Authors:
    Sachin Cherian
"""

import os
from datetime import datetime as dt

from speck import FileCacheManager
from matplotlib import pyplot

__all__ = [
    'plot',
    'Tracker'
]

def plot(tracker, name):
    """Plot all values of temp_c stored by ``tracker``."""

    raw = sorted(tracker.find_all(name), key=lambda x: x[0])
    # strftime formats the datetime object into a string
    pyplot.plot([i[0].strftime("%Y-%m-%d") for i in raw], [i[1].temp_c.val for i in raw])
    pyplot.title(name)
    pyplot.show()

class Tracker:
    """Utility to dump speck objects into cache files, stored per day, in a "tracker directory"."""

    def __init__(self, path='.tracker'):
        self.path = path
        self.cache = FileCacheManager(self.path)

    def dump(self, name, data):
        """Dump an object into the tracker directory."""
        self.cache.dump(name + '-' + str(dt.now()).split(" ")[0], data)

    def find_all(self, name):
        """Find all dumped objects in the tracker directory."""

        return (
            (dt.strptime(i.replace(name, ''), "-%Y-%m-%d.dat"), self.cache.read(i.rstrip('.dat')))
            for i in os.listdir(self.path)
            if i.startswith(name)
        )
