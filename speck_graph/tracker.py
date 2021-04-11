from speck_wa.cache import Cache

import os
from datetime import datetime as dt

class Tracker:
    """Utility to dump speck objects into cache files, stored per day."""

    def __init__(self, path='cache/tracker'):
        self.path = path
        self.cache = Cache(self.path)

    def dump(self, name, data):
        """Dump the speck object."""
        self.cache.dump(name + '-' + str(dt.now()).split(" ")[0], data)

    def find_all(self, name):
        """Find all dumped speck objects."""

        results = []
        
        for i in os.listdir(self.path):
            if i.startswith(name):
                results.append((dt.strptime(i.replace(name, ''), "-%Y-%m-%d.dat"), self.cache.read(i.rstrip('.dat'))))

        return results