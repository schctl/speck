"""
Frontend for speck.

Authors:
    Nevin Jose
    Sachin Cherian
"""

import os

# -- Profiling --
import io
import pstats
import cProfile
# ---------------

from speck_app.app import SpeckApp

def _rootd(path):
    """Return absolute path of `path` relative to this file."""
    return os.path.join(os.path.dirname(__file__), path)

def vanilla_profile(func):
    """Profile a function."""
    def inner(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()

        func(*args, **kwargs)

        profile.disable()

        buffer = io.StringIO()
        profile_stats = pstats.Stats(profile, stream=buffer).sort_stats('cumulative')

        if 'SPECK_DEBUG' in os.environ:
            profile_stats.print_stats()
            print(buffer.getvalue())

    return inner

@vanilla_profile
def main():
    """Run the sample frontend app."""
    with open(_rootd('token.txt')) as f:
        app = SpeckApp(f.read().rstrip()) # Create an instance
        app.run()

if __name__ == '__main__':
    main()
