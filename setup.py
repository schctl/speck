import os
from setuptools import setup

def readf(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name     = "speck",
    version  = readf('VERSION')[0],
    license  = "MIT",
    author   = "Nevin Jose, Sachin Cherian",
    url      = "https://github.com/schctl/speck",
    packages = [
        "speck",
        "speck.cache",
        "speck.waw",
        "speck.waw.types",
        "speck.ext",
        "speck.ext.track",
        "speck.ext.gui",
        ],
    package_data = {'': ['etc/*', 'etc/exports/*']},
    include_package_data = True,
    description      = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README.md'),
    install_requires = list(readf('requirements.txt').splitlines()),
    python_requires  = ">=3.6.0"
)
