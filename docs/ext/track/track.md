Package \<`track`\>
===================
Utility module to keep track of temperature per location and graph them.

#

<sup>*method*</sup> `plot(tracker, name)`
-----------------
Plot all values of temp_c stored by `tracker`.

### Parameters
- `tracker`
<br>        Tracker object. Anything that implements the `find_all(self, name)` method.

- `name`: `str`
<br>        Name of the location to plot.


<sup>*class*</sup> `Tracker`
-------------------
Utility to dump speck objects into cache files, stored per day, in a "tracker directory".

### `__init__(self, path='.tracker')`

### Attributes
- `path`: `str`
<br>        Path to the cache directory for tracked files.

- `cache`: [`Cache`](../cache/cache.md)

### Methods
- `dump(self, name, data)`
<br>        Dump an object into the tracker directory.

- `find_all(self, name)` -> `list[<object>]`
<br>        Find all dumped objects in the tracker directory.
