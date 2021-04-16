[//]: # (Speck is a minimal wrapper and frontend for weatherAPI.com)

<h1 align="center">Speck</h1>
<p align="center">Minimal wrapper and frontend for <a href="https://www.weatherapi.com/">weatherAPI.com</a></p>
<p align="center">
    <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/schctl/speck?style=for-the-badge"></a>
    <a href="https://speck.readthedocs.io/en/latest/"><img alt="Read the Docs" src="https://img.shields.io/readthedocs/speck?style=for-the-badge"></a>
    <a href="https://github.com/schctl/speck/releases"><img alt="TAG" src="https://img.shields.io/github/v/tag/schctl/speck?label=Latest&style=for-the-badge"></a>
    <a href="https://lgtm.com/projects/g/schctl/speck/context:python"><img alt="LGTM Grade" src="https://img.shields.io/lgtm/grade/python/github/schctl/speck?label=Code&style=for-the-badge"></a>
    <a href="https://github.com/schctl/speck"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/schctl/speck?label=Stars&logo=GitHub&style=for-the-badge"></a>
</p>

## Usage

### Installation

Speck can be installed as a library. First clone the repository.

    git clone https://github.com/schctl/speck.git

Then, from the root directory, run

    pip install .

### GUI Frontend

To run the speck app, run `__main__.py` under `app`.

    python app

The `speck` library must be installed for this to work, in addition to requirements listed in `requirements.txt`.

    pip install -r requirements.txt

The username and password entry screen is only intended as a dummy. To make the app ignore this,
set the `SPECK_DEV` environment variable. The username and password are `11C` and `11c2021`.

## City Data

City data is from [`cities.json`](https://github.com/lutangar/cities.json), and has been edited to remove irrelevant data.
