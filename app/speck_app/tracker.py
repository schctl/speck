"""
Tracker class.
"""

import os
from datetime import datetime as dt
from datetime import timedelta as td

from matplotlib import pyplot

from speck import FileCacheManager

__all__ = [
    'plot',
    'Tracker'
]

# Plot -----------

def plot(forecast, tracker, name):
    """Plot all values of ``temp_c`` stored by ``tracker``."""

    raw = sorted(tracker.find_all(name), key=lambda x: x[0])

    # strftime formats the datetime object into a string
    pyplot.plot(
        [i[0].strftime("%Y-%m-%d") for i in raw],
        [i[1].temp_c.val for i in raw]
    )
    pyplot.plot(
        [(dt.now() + td(days=i)).strftime("%Y-%m-%d") for i in range(len(forecast))],
        [i.day.avgtemp_c.val for i in forecast],
        linestyle='dashed'
    )

    pyplot.title(name)
    pyplot.show()

# ----------------

class Tracker:
    """Utility to dump speck objects into cache files, stored per day, in a "tracker directory"."""

    def __init__(self, path='.tracker'):
        self._path = path
        self.cache = FileCacheManager(self._path)

    @property
    def path(self):
        """Get the path to the data files stored by this Tracker."""
        return self._path

    def dump(self, name, data):
        """Dump an object into the tracker directory."""
        self.cache.dump(name + '-' + dt.now().strftime("%Y-%m-%d"), data)

    def find_all(self, name):
        """Find all dumped objects in the tracker directory."""

        return (
            (dt.strptime(i.replace(name, ''), "-%Y-%m-%d.dat"), self.cache.read(i.rstrip('.dat')))
            # ^ format string into a datetime object
            for i in os.listdir(self.path)
            if i.startswith(name)
        )
