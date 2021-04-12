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
    packages         = ["waw", "ui", "tracker", "cache"],
    description      = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README.txt'),
    install_requires = list(readf('requirements.txt').splitlines())
)
