# Package \<`types`\>
Utility types to hold weatherapi information.

## Unit types

class \<`Km`\>
--------------
Kilometer.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `mi(self)` -> `float`
<br>    Equivalent Miles.

class \<`Mm`\>
--------------
Millimeter.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `inches(self)` -> `float`
<br>    Equivalent Inches.

class \<`Mb`\>
--------------
Milibar.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `inches(self)` -> `float`
<br>    Equivalent Inches of Mercury.

class \<`Cel`\>
---------------
Celsius.

### `__init__(self, val: float)`

### Attributes
- `val`: `float`

### Methods
- `fahrenheit(self)` -> `float`
<br>    Equivalent Fahrenheit.
- `kelvin(self)` -> `float`
<br>    Equivalent Kelvin.

#

## WeatherAPI return types

class \<`BasePoint`\>
---------------------
Abstract class representing a single data point.

## Methods
- `from_raw(cls, location, data: dict)` -> `BasePoint`
<br>    Return new instance from weatherapi response.

- `from_json(cls, location, data: str)` -> `BasePoint`
<br>    Return new instance of child from raw `weatherapi` response.

- `to_bytes(self)` -> [Pickled Object](https://docs.python.org/3/library/pickle.html#pickle.dump)
<br>    Return a  bytes-like object.

class \<`Location(BasePoint)`\>
---------------------
Represents location data such as coordinates, time zone, region, at a particular time.

## Attributes
- `lat`
- `lon`
- `name`
- `region`
- `country`
- `tz_id`: `str`
- `localtime`: [`datetime.datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)

## Methods
- `from_raw(cls, data: dict)` -> `Location`
<br>    Return new instance from weatherapi response.

- `from_json(cls, data)` -> `Location`
<br>    Return new instance from raw `weatherapi` response.

- `to_bytes(self)` -> [Pickled Object](https://docs.python.org/3/library/pickle.html#pickle.dump)
<br>    Return a  bytes-like object.

class \<`HourlyPoint(BasePoint)`\>
---------------------
Abstract class representing a single data point.

## Attributes
- location = Location.from_raw(location)
- time
- temp_c = Cel(temp_c)
- feelslike_c = Cel(feelslike_c)
- windchill_c = Cel(windchill_c)
- heatindex_c = Cel(heatindex_c)
- dewpoint_c = Cel(dewpoint_c)
- condition = condition
- wind_kph = Km(wind_kph)
- gust_kph = Km(gust_kph)
- wind_degree = wind_degree
- wind_dir = wind_dir
- pressure_mb = Mb(pressure_mb)
- precip_mm = Mm(precip_mm)
- will_it_rain = will_it_rain
- will_it_snow = will_it_snow
- chance_of_rain = chance_of_rain
- chance_of_snow = chance_of_snow
- humidity = humidity
- cloud = cloud
- is_day = bool(is_day)
- uv = uv
- vis_km = Km(vis_km)