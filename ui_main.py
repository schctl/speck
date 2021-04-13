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

from ext.gui.frontend import SampleFrontend

if __name__ == '__main__':
    profile = cProfile.Profile()
    profile.enable()

    app = SampleFrontend() # Create an instance
    app.run()

    profile.disable()

    buffer = io.StringIO()
    profile_stats = pstats.Stats(profile, stream=buffer).sort_stats('cumulative')

    if 'SPECK_DEBUG' in os.environ:
        profile_stats.print_stats()
        print(buffer.getvalue())
