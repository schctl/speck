<h1 align="center">Speck</h1>

<p align="center">Minimal wrapper and frontend for <a href="https://www.weatherapi.com/">weatherAPI.com</a></p>

<p align="center">
    <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/schctl/speck?style=for-the-badge"></a>
    <a href="https://lgtm.com/projects/g/schctl/speck/context:python"><img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/schctl/speck?label=Code&style=for-the-badge"></a>
    <a href="https://github.com/schctl/speck"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/schctl/speck?label=Stars&logo=GitHub&style=for-the-badge"></a>
    <a href="https://github.com/schctl/speck/releases"><img alt="TAG" src="https://img.shields.io/github/v/tag/schctl/speck?label=Latest&style=for-the-badge"></a>
</p>

## City Data

City data is from [`cities.json`](https://github.com/lutangar/cities.json), and has been edited to remove irrelevant data.

## Usage

### GUI Frontend

Run the frontend with:

    python ui_main.py

The username and password entry screen is only intended as a dummy. To bypass this,
set the `SPECK_DEV` environment variable.

### Documentation

Documentation is available in markdown format [here](docs/README.md).

### Requirements

Install requirements by running:

    pip install -r requirements.txt

Additionally, [`tkinter`](https://wiki.python.org/moin/TkInter) is required, for [`ext.gui`](docs/ext/gui/gui.md).

### Installation

To install speck, first clone the repository.

    git clone https://github.com/schctl/speck

Then, from the root directory, run

    pip install .


## Other links

- [Lgtm Code Analysis](https://lgtm.com/projects/g/schctl/speck/context:python)
- [Project wiki](https://github.com/schctl/speck/wiki)
