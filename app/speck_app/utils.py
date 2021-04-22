"""
Commonly used functions.
"""

import os
from hashlib import md5

def rootd(path):
    """Return absolute path of `path` relative to this file."""
    return os.path.join(os.path.dirname(__file__), path)

def readf(fname):
    """Utility function to read a file."""
    with open(fname, 'r') as f:
        return f.read()

def utf8_to_md5_hex(string):
    """Convert a UTF-8 encoded string to its md5 in hex format."""
    return md5(bytes(string, 'utf-8')).hexdigest()
