"""
Cache utility to store and keep track of objects by name.
"""

# Cache is used in this library for the purpose of reducing API calls,
# which can only be used a limited amount of times per month/
# API response's are stored in "cache files", which can be read later on.

from .cache import *
