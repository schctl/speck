#!/usr/bin/env python
"""
Runs the speck frontend.
"""

import os

# -- Profiling --
import io
import pstats
import cProfile
# ---------------

from speck_app import utils
from speck_app.app import SpeckApp

def vanilla_profile(func):
    """Profile a function."""
    def inner(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()

        func(*args, **kwargs)

        profile.disable()

        buffer = io.StringIO()  # StringIO acts as a File like object
        profile_stats = pstats.Stats(profile, stream=buffer).sort_stats('cumulative')

        if 'SPECK_DEV' in os.environ:
            profile_stats.print_stats()
            print(buffer.getvalue())

    return inner

@vanilla_profile
def main():
    """Run the sample frontend app."""
    with open(utils.rootd('../token.txt')) as f:
        app = SpeckApp(f.read().rstrip()) # Create an instance
        app.run()

if __name__ == '__main__':
    main()
