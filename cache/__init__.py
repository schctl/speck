"""
Cache utility to store and keep track on objects
by name.
"""

import os
import json
import pickle

from pathlib import Path

from datetime import datetime as dt
import zlib

__authors__ = ['Sachin Cherian']

# Cache is used in this library for the purpose of reducing API calls,
# which can only be used a limited amount of times per month/
# API response's are stored in "cache files", which can be read later on.

class Cache:
    """Cache Manager utility. Keeps track of and gets/updates data from cache files."""

    def __init__(self, path):
        self.path = path

        Path(path).mkdir(parents=True, exist_ok=True) # Creates cache folder

        ## Cache is identified with its `name` attribute. Cache can be read by keeping track of this
        ## value and reading it with `read` later on.

    def read(self, name):
        """Tries to read cache with `name`. Returns `None` if no such file is found."""
        try:
            with open(f"{self.path}/{name}.dat", "rb") as f: # Cache is stored as a dictionary/list
                try:                                         # in a binary file, which can be read later on.
                    return pickle.loads(zlib.decompress(pickle.load(f)))
                except:
                    pass

        except pickle.PickleError:
            pass
        except FileNotFoundError:
            pass

        return

    def dump(self, name, data):
        """Writes data to a cache file with `name`. `name` must be kept track of manually."""
        with open(f"{self.path}/{name}.dat", "wb") as f:
            pickle.dump(zlib.compress(pickle.dumps(data)), f)

    def cleanup(self, name):
        """Cleans up all cache files with a given `name`. Supports wildcard (*) deletion."""
        els = name.split('*')

        # Removes all cache files matching the `name` pattern. `*` represents any set of characters.

        try:
            for i in os.listdir(self.path):
                for n, j in enumerate(els):
                    if not (j in i and (i.index(j) <= i.index(els[min(n, len(name) - 1)]) or j == '')):
                        break  # NEED to cleanup - written at 4 am
                else:
                    os.remove(f"{self.path}/{i}") # Delete the actual file

        except FileNotFoundError:
            pass
