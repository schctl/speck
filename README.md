[//]: # (Speck is a minimal wrapper and frontend for weatherAPI.com)

# Speck

<a href="https://pypi.org/project/speck-wrapper/"><img alt="PyPI" src="https://img.shields.io/pypi/v/speck-wrapper?style=for-the-badge" height="24"></a>
<a href="https://lgtm.com/projects/g/schctl/speck/context:python"><img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/schctl/speck?label=Code&style=for-the-badge" height="24"></a>
<a href="https://speck.readthedocs.io/en/latest/"><img alt="Read the Docs" src="https://img.shields.io/readthedocs/speck?style=for-the-badge" height="24"></a>

Minimal wrapper and frontend for [weatherAPI.com](https://www.weatherapi.com/)

[Wiki](https://github.com/schctl/speck/wiki)

## Usage

**__Installation__**

Speck is packaged publicly on PyPi as [`speck-wrapper`](https://pypi.org/project/speck-wrapper/)

    pip install speck-wrapper

To install from source, first clone the repository

    git clone https://github.com/schctl/speck.git

Then, from the root directory, run

    pip install .

**__Usage__**

`speck` can be imported as a regular python module after installation.

    >>> import speck
    >>> help(speck)

## GUI Frontend

**__Installation__**

Install scripts in `scripts` will automate the install for you.

**__Manual installation__**

The `speck` library must be installed for this to work, in addition to requirements listed in `app/requirements.txt`.

    pip install -r app/requirements.txt

**__Usage__**

To run the speck app, run `main.py` under `app`.

    cd app && python main.py

The username and password entry screen is a dummy. To make the app ignore this, set the `SPECK_DEV` environment variable. The username and password are `11C` and `11c2021`.
