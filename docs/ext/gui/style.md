Module \<`style`\>
==================
Window styling utilities.


<sup>*class*</sup> `WindowStyle`
-------------------------------
Details about the main window.

### Attributes
- `width`: `int`
- `height`: `int`

<sup>*class*</sup> `FontStyle`
-------------------------------
Details about fonts to be used.

### Attributes
- `family`: `str`
- `size_big`: `int`
- `size_medium`: `int`
- `size_smalll`: `int`

<sup>*class*</sup> `ColorStyle`
-------------------------------
Details for colors to be used.

### Attributes
- `fg`: `str`
- `bg`: `str`

<sup>*class*</sup> `SpeckStyle`
-------------------------------
Container around all other styles.

### Attributes
- `window`: `WindowStyle`
- `fonts`: `dict[FontStyle]`
- `colors`: `dict[ColorStyle]`

### Methods
- `from_file(cls, file)`
<br>        Create an instance of `SpeckStyle`, with details read from a file with data in json format.
