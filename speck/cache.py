"""
Cache utility.
The primary purpose of this is to reduce the number of required API calls.
"""

import os

import zlib
import pickle

from pathlib import Path

__all__ = [
    'FileCacheManager'
]

class BufferedCacheManager:
    """
    Buffered Cache Manager implementation. Keeps track of cache in memory.
    """

    def __init__(self, path):
        raise NotImplementedError

class FileCacheManager:
    """
    File based Cache Manager implementation. Keeps track of and gets/updates data from cache files.

    :param path: Path to the "cache directory". Cache files will be stored here.
    """

    def __init__(self, path):
        self._path = path

        Path(path).mkdir(parents=True, exist_ok=True) # Creates cache folder

        ## Cache is identified with its `name` attribute. Cache can be read by keeping track of this
        ## value and reading it with `read` later on.

    @property
    def path(self):
        """
        Returns the directory to which cache files are being stored.

        :rtype: :class:`str`
        """
        return self._path

    def find_all(self):
        """Return a list of all tracked cache files."""

        return (
            i.rstrip('.dat')
            for i in os.listdir(self._path)
        )

    def read(self, name):
        """Tries to read cache with ``name``. Returns ``None`` if no such file is found."""

        try:
            # Cache is stored as an object in a binary file,
            # which can be loaded into an object directly later on.
            with open(f"{self._path}/{name}.dat", "rb") as f:
                return pickle.loads(zlib.decompress(pickle.load(f)))

        except pickle.PickleError:
            pass
        except FileNotFoundError:
            pass

        return None

    def dump(self, name, data):
        """Writes data to a cache file with ``name``. ``name`` must be kept track of manually."""

        with open(f"{self._path}/{name}.dat", "wb") as f:
            pickle.dump(zlib.compress(pickle.dumps(data)), f)

    def cleanup(self, name):
        """Cleans up all cache files with a given ``name``. Supports wildcard (*) deletion."""

        els = name.split('*') # splits across *, - removes the * as well

        # Removes all cache files matching the `name` pattern. `*` represents any set of characters.

        try:
            for i in os.listdir(self._path):
                for n, j in enumerate(els):
                    i = i.rstrip('.dat')
                    if not (
                        j == '' or ( j in i and \
                            (i.index(j) >= i.index(els[0 if n < 1 else n - 1]))
                            )
                        ):
                        break

                        # Explanation for above check
                        # ---------------------------
                        # `els` is a list of all components split across *.
                        # We check if each component of `else` is in
                        # the file name being checked (`j in i`).
                        # If the component is empty, we can skip directly.
                        # If it is, we make sure its after the previous
                        # component (second check).
                else:
                    os.remove(f"{self._path}/{i}") # Delete the actual file

        except FileNotFoundError:
            pass
