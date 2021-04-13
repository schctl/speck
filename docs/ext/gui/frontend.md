Module \<`frontend`\>
=====================
Sample tkinter frontend for speck.

#

<sup>*class*</sup> `SampleFrontend`
-----------------------------------
Implementation for a sample frontend.

### `__init__(self, token, auth_file=_rootd('etc/auth.txt'))`
- `token` is the path to the weatherapi key.
- `auth_file` is the path to file containing auth tokens (two - username and password in separate lines), in md5 hex format.

### Methods
- `welcome(self)`
<br>        Implementation for Welcome screen.

- `location_entry(self)`
<br>        Implementation for Location Entry Screen.

- `info_screen(self, loc)`
<br>        Display information for a location.

- `run(self)`
<br>        Run the application.