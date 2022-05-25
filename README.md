# speck

`speck` is a minimal weather app and library to interact with [weatherapi.com]. It was created by
[Sachin Cherian](https://github.com/schctl/) and [Nevin Jose](https://github.com/FaZe-Vulcan/)
as their 12th grade Computer Science project and showcases some concepts in Python and
some popular development ideas.

Some of the main ideas demonstrated are:
- Usage of functions and classes in Python
- Using packages and modules in Python to separate functionality in code
- Distributing code as packages
- Retrieving and storing data from a remote source
- Serving that data using a GUI toolkit such as [Tkinter], and visualization with [matplotlib]
- Using [Version Control] software like [git] to keep track of development and help with collaboration.

See the [Wiki] for more documentation on some concepts.

Since the project has been completed, this repository will no longer be maintained.

---

[<img alt="PyPI" src="https://img.shields.io/pypi/v/speck-wrapper?style=for-the-badge" height="24">](https://pypi.org/project/speck-wrapper/)
[<img alt="LGTM" src="https://img.shields.io/lgtm/grade/python/github/schctl/speck?style=for-the-badge" height="24">](https://lgtm.com/projects/g/schctl/speck/)
[<img alt="Read the Docs" src="https://img.shields.io/readthedocs/speck?style=for-the-badge" height="24">](https://speck.readthedocs.io/en/latest/)

## Usage

### The speck library

Speck is packaged publicly on PyPi as [`speck-wrapper`]

```
pip install speck-wrapper
```

Alternatively, to install from source, first clone the repository and then use `pip` to install it.

```
git clone https://github.com/schctl/speck.git
cd speck
pip install .
```

`speck` can then be imported as a regular python module.

```py
>>> import speck
>>> help(speck)
```

### GUI Frontend

The `speck` library must be installed for this to work, in addition to requirements listed in `app/requirements.txt`.

```
# From the repository's root directory
pip install -r app/requirements.txt
```

To run the speck app, run `main.py` under `app`.

```
cd app && python main.py
```

The username and password entry screen is a dummy. The username and password are `11C` and `11c2021`.
Set the `SPECK_DEV` environment variable to make the app ignore the login screen.

[wiki]: https://github.com/schctl/speck/wiki/
[weatherapi.com]: https://www.weatherapi.com/
[`speck-wrapper`]: https://pypi.org/project/speck-wrapper/
[tkinter]: https://docs.python.org/3/library/tkinter.html
[matplotlib]: https://matplotlib.org/
[git]: https://git-scm.com/
[version control]: https://en.wikipedia.org/wiki/Version_control
