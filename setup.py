import os
import re

from setuptools import setup

def readf(fname):
    print(os.path.join(os.path.dirname(__file__), fname))
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()

def get_version(fname):
    return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', readf(fname), re.MULTILINE).group(1)
    # re.MULTILINE tells `search` to compare each line instead of the whole text.
    # \s - whitespace character
    # [\'"] - either ' or "
    # ([^\'"]*) - characters that are NOT ' or "
    # .group(1) will return the first subgroup of the match - subgroups are enclosed in `()`

setup(
    name     = "speck",
    version  = get_version('speck/__init__.py'),
    license  = "MIT",
    author   = "Nevin Jose, Sachin Cherian",
    description      = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README.md'),
    long_description_content_type = 'text/markdown',
    url      = "https://github.com/schctl/speck",
    packages = [
        "speck",
        "speck.types"
        ],
    package_data = {'': ['LICENSE', 'README.md', 'speck/etc/*']},
    include_package_data = True,
    install_requires = list(readf('requirements.txt').splitlines()),
    python_requires  = ">=3.6.0"
)
