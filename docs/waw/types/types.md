# Package \<`types`\>
Utility types to hold weatherapi information.

#

## Unit types

<sup>*class*</sup> `Km`
--------------
Kilometer.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `mi(self)` -> `float`
<br>        Equivalent Miles.

<sup>*class*</sup> `Mm`
--------------
Millimeter.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `inches(self)` -> `float`
<br>        Equivalent Inches.

<sup>*class*</sup> `Mb`
--------------
Milibar.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `inches(self)` -> `float`
<br>        Equivalent Inches of Mercury.

<sup>*class*</sup> `Cel`
---------------
Celsius.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `fahrenheit(self)` -> `float`
<br>        Equivalent Fahrenheit.
- `kelvin(self)` -> `float`
<br>        Equivalent Kelvin.

#

## WeatherAPI return types

<sup>*class*</sup> `BasePoint`
---------------------
Abstract class representing a single data point.

### Methods
- `from_raw(cls, location, data: dict)` -> `BasePoint`
<br>        Return new instance from weatherapi response.

- `from_json(cls, location, data: str)` -> `BasePoint`
<br>        Return new instance of child from raw `weatherapi` response.

- `to_bytes(self)` -> [Pickled Object](https://docs.python.org/3/library/pickle.html#pickle.dump)
<br>        Return a  bytes-like object.

<sup>*class*</sup> `Location(BasePoint)`
---------------------
Represents location data such as coordinates, time zone, region, at a particular time.

### Attributes
- `lat`
- `lon`
- `name`
- `region`
- `country`
- `tz_id`: `str`
- `localtime`: [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)

### Methods
- `from_raw(cls, data: dict)` -> `Location`
<br>        Return new instance from weatherapi response.

- `from_json(cls, data)` -> `Location`
<br>        Return new instance from raw `weatherapi` response.

- `to_bytes(self)` -> [Pickled Object](https://docs.python.org/3/library/pickle.html#pickle.dump)
<br>        Return a  bytes-like object.

<sup>*class*</sup> `HourlyPoint(BasePoint)`
---------------------
Represents weather data at a particular time in some location.

### Attributes
- `location`: `Location`
- `time`: [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)
- `temp_c`: `Cel`
- `feelslike_c`: `Cel`
- `windchill_c`: `Cel`
- `heatindex_c`: `Cel`
- `dewpoint_c`: `Cel`
- `condition`: `str`
- `wind_kph`: `Km`
- `gust_kph`: `Km`
- `wind_degree`
- `wind_dir`
- `pressure_mb`: `Mb`
- `precip_mm`: `Mm`
- `will_it_rain`
- `will_it_snow`
- `chance_of_rain`
- `chance_of_snow`
- `humidity`
- `cloud`
- `is_day`
- `uv`
- `vis_km`: `Km`

<sup>*class*</sup> `DayPoint(BasePoint)`
---------------------
The total conditions per day.

### Attributes
- `location`: `Location`
- `maxtemp_c`: `Cel`
- `mintemp_c`: `Cel`
- `avgtemp_c`: `Cel`
- `condition`
- `maxwind_kph`: `Km`
- `totalprecip_mm`: `Mm`
- `avgvis_km`: `Km`
- `avghumidity`
- `uv`

<sup>*class*</sup> `AstroPoint(BasePoint)`
---------------------
Astronomy information.

### Attributes
- `location`: `Location`
- `sunrise`
- `sunset`
- `moonrise`
- `moonset`
- `moon_phase`

<sup>*class*</sup> `DailyPoint(BasePoint)`
---------------------
All information per day, inlcuding hourly info.

### Attributes
- `location`: `Location`
- `day`: `DayPoint`
- `hour`: `HourlyPoint`
- `astro`: `AstroPoint`

<sup>*class*</sup> `IpPoint(BasePoint)`
---------------------
IP Address information.

### Attributes
- `location`: `Location`
- `ip`: `str`
- `type`: `str`
<br>        Type of IP (ipv4 or ipv6)

### Methods
- `from_raw(cls, data: dict)` -> `Location`
<br>        Return new instance from weatherapi response.

- `from_json(cls, data)` -> `Location`
<br>        Return new instance from raw `weatherapi` response.

<sup>*class*</sup> `SportsPoint(BasePoint)`
---------------------
IP Address information.

### Attributes
- `stadium`: `str`
- `country`: `int`
- `region`: `str`
- `tournament`: `str`
- `start`: `str`
- `match`: `str`

### Methods
- `from_raw(cls, data: dict)` -> `Location`
<br>        Return new instance from weatherapi response.

- `from_json(cls, data)` -> `Location`
<br>        Return new instance from raw `weatherapi` response.
