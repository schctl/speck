<h1 style="text-align: center;">Speck</h1>

<p style="text-align: center;">Minimal wrapper and frontend for <a href="https://www.weatherapi.com/">weatherAPI.com</a>.</p>

<p style="text-align: center;">
    <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/schctl/speck?style=for-the-badge"></a>
    <a href="https://github.com/schctl/speck/releases"><img alt="TAG" src="https://img.shields.io/github/v/tag/schctl/speck?style=for-the-badge"></a>
    <a href="https://lgtm.com/projects/g/schctl/speck/context:python"><img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/schctl/speck?style=for-the-badge"></a>
</p>

Speck's focus isn't usability, rather, to show use of application structure, version control,
and other common practices used in open source projects. It intends to have a well documented
API and have thoroughly commented implementations. It also has a repository hosted on GitHub.

    https://github.com/schctl/speck

### City Data

City data is from [`cities.json`](https://github.com/lutangar/cities.json), and has been edited to remove irrelevant data.

### Usage

Run the frontend with:

    python ui_main.py

The username and password entry screen is only intended as a dummy. To bypass this,
set the `SPECK_DEV` environment variable.

#### Documentation

Documentation is available in markdown format [here](docs/README.md).

#### Requirements

Install requirements by running:

    pip install -r requirements.txt

Additionally, [`tkinter`](https://wiki.python.org/moin/TkInter) is required.


### Other links

- [Lgtm Code Analysis](https://lgtm.com/projects/g/schctl/speck/context:python)
- [Project wiki](https://github.com/schctl/speck/wiki)
