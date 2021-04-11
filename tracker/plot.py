from . import Tracker

from matplotlib import pyplot

def plot(tracker: Tracker, name):
    """Plot all values of temp_c stored by `tracker`."""
    raw = sorted(tracker.find_all(name), key=lambda x: x[0])

    pyplot.plot([i[0].strftime("%Y-%m-%d") for i in raw], [i[1].temp_c.val for i in raw])
    pyplot.title(name)
    pyplot.show()