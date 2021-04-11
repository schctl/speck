from ..speck.cache import Cache

import os
from datetime import datetime as dt

class Tracker:
    def __init__(self, path='cache/tracker'):
        self.path = path
        self.cache = Cache(self.path)

    def dump(self, name, data):
        cache.dump(name + str(dt.now()).split(" ")[0], data)

    def find_all(self, name):
        results = []
        for i in os.listdir(self.path):
            if i.startswith(name):
                results.append(self.cache.read(i))

        return results