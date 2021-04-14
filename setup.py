import os
from setuptools import setup

def readf(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name     = "speck",
    version  = readf('VERSION')[0],
    license  = "MIT",
    author   = "Nevin Jose, Sachin Cherian",
    description      = "A simple wrapper and frontend for weatherAPI.com",
    long_description = readf('README.md'),
    long_description_content_type = 'text/markdown',
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
    package_data = {'': ['LICENSE', 'README.md', 'etc/*', 'etc/exports/*']},
    include_package_data = True,
    install_requires = list(readf('requirements.txt').splitlines()),
    python_requires  = ">=3.6.0"
)
