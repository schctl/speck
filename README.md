# Speck

Minimal wrapper and frontend for weatherAPI.com.

    https://www.weatherapi.com/

Speck's focus isn't usability, rather, to show use of application structure, version control,
and other common practices used in open source projects. It intends to have a well documented
API and have thoroughly commented implementations. It also has a repository hosted on GitHub.

    https://github.com/schctl/speck

## Documentation

Documentation is available in markdown files [here](docs/README.md).

## City Data

City data is from cities.json, and has been edited to remove irrelevant data.

    https://github.com/lutangar/cities.json

## Requirements

Install requirements by running:

    pip install -r requirements.txt

Additionally, tkinter is required.

    https://wiki.python.org/moin/TkInter

## Usage

Run the frontend with

    python ui_main.py

The username and password entry screen is only intended as a dummy. To bypass this,
set the `SPECK_DEV` environment variable.

## Other links

Lgtm Code Analysis

    https://lgtm.com/projects/g/schctl/speck/context:python

Project wiki

    https://github.com/schctl/speck/wiki
