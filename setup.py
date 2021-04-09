import os
from setuptools import setup

def readf(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

deps_required = list(readf('requirements.txt').splitlines())

setup(
    name             = "speck",
    version          = readf('VERSION')[0],
    license          = "MIT",
    author           = "Nevin Jose, Sachin Cherian",
    url              = "https://github.com/schctl/speck",
    packages         = ["speck", "speck_ui"],
    description      = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README'),
    install_requires = deps_required
)
