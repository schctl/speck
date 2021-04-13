Package \<`cache`\>
===================

Utilities to store objects in "cache files". This package's primary purpose to reduce the amount of API calls required by [`waw`](../waw/waw.md)


<sup>*class*</sup> `Cache`
-----------------
Cache Manager utility. Keeps track of and gets/updates data from cache files.

### Attributes
- `path`: `str`
<br>        Path to cache directory.

### Methods
- `find_all(self)` -> `list[str]`
<br>        Return a list of all tracked Cache files.

- `read(self, name)` -> `<object>`
<br>        Tries to read cache with `name`. Returns `None` if no such file is found.

- `dump(self, name, data)`
<br>        Writes data to a cache file with `name`. `name` must be kept track of manually.

- `cleanup(self, name)`
<br>        Cleans up all cache files with a given `name`. Supports wildcard (*) deletion.