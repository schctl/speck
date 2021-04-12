"""Plot a graph from data stored by a `Tracker`."""

from matplotlib import pyplot

from . import Tracker

def plot(tracker: Tracker, name):
    """Plot all values of temp_c stored by `tracker`."""
    raw = sorted(tracker.find_all(name), key=lambda x: x[0])

    # strftime formats the datetime object into a string
    pyplot.plot([i[0].strftime("%Y-%m-%d") for i in raw], [i[1].temp_c.val for i in raw])
    pyplot.title(name)
    pyplot.show()
