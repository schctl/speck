"""Tracker class."""

import os
from datetime import datetime as dt

from speck.cache import Cache

class Tracker:
    """Utility to dump speck objects into cache files, stored per day, in a "tracker directory"."""

    def __init__(self, path='.tracker'):
        self.path = path
        self.cache = Cache(self.path)

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
