import os
from setuptools import setup

def readf(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name             = "speck",
    version          = readf('VERSION')[0],
    license          = "MIT",
    author           = "Nevin Jose, Sachin Cherian",
    url              = "https://github.com/schctl/speck",
    packages         = [
        "speck",
        "speck.waw",
        "speck.ext",
        "speck.ext.cache",
        "speck.ext.track",
        "speck.ext.gui"
        ],
    description      = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README.txt'),
    install_requires = list(readf('requirements.txt').splitlines()),
    python_requires  = ">=3.6.0"
)
