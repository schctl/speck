"""
Commonly used functions.
"""

import os
from hashlib import sha256

__all__ = [
    'rootd',
    'readf',
    'utf8_to_sha256'
]

def rootd(path):
    """Return absolute path of `path` relative to this file."""
    return os.path.join(os.path.dirname(__file__), path)

def readf(fname):
    """Utility function to read a file."""
    with open(fname, 'r') as f:
        return f.read()

def utf8_to_sha256(string):
    """Convert a UTF-8 encoded string to its sha256 in hex format."""
    return sha256(bytes(string, 'utf-8')).hexdigest()
