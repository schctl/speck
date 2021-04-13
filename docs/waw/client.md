# Module \<`client`\>

<sup>*class*</sup> `Client`
==================
HTTPS client used to request data from weatherapi.com

### `__init__(self, token, use_cache = False, cache_path = '.cache')`


## Attributes

### `token`: `str`
API token used to make weatherAPI requests with.

### `session`: [`requests.Session`](https://docs.python-requests.org/en/master/user/advanced/#session-objects)
https session kept-alive to make calls with.


## Methods

- All methods have the possibility of raising a [`WeatherApiError`](errors.md)

### `find_city(self, loc: str)` -> `list[str]`
Try to find a city with a match from a known list of [locations](../../speck/etc/cities_p.json). This method is highly unlikely to be used frequently, since weatherAPI tries to interpret location names even if incorrect, but is provided anyway.


### `current(self, loc: str)` -> [`HourlyPoint`](types/types.md)
Get current weather conditions in a location.

#### Parameters
- `loc`: Query location to find data for. It could be following:
    - Latitude and Longitude (Decimal degree). e.g.:'48.8567,2.3508'
    - city name e.g.: 'Paris'
    - US zip e.g.: '10001'
    - UK postcode e.g: 'SW1'
    - Canada postal code e.g: 'G2J'
    - metar:<metar code> e.g: 'metar:EGLL'
    - iata:<3 digit airport code> e.g: 'iata:DXB'
    - auto:ip IP lookup e.g: 'auto:ip'
    - IP address (IPv4 and IPv6 supported) e.g: '100.0.0.1'


### `forecast(self, loc: str, days=3)` -> [`list[DailyPoint]`](types/types.md)
Get weather forecast for a location.

#### Parameters
- `loc`: See docs on method `current`.
- `days`: Number of days to restrict the forecast for. weatherAPI allows up to 10 days, but it in practice the maximum is 3.


### `astronomy(self, loc)` -> [`AstroPoint`](types/types.md)
Get astronomy information for a location.

#### Parameters
- `loc`: See docs on method `current`.

#### Aliases
- `astro`


## **The below implementations have not been tested.**


### `ip_lookup(self, ip)` -> [`IpPoint`](types/types.md)
Get information for an IP address.

#### Parameters
- `ip`: IPv6 or IPv4 string.

#### Aliases
- `ip`


### `search(self, loc: str)` -> [`list[Location]`](types/types.md)
Get a list of location objects based on query parameter.

#### Parameters
- `loc`: See docs on method `current`.


### `timezone_info(self, loc: str)` -> [`Location`](types/types.md)
Get timezone and associated information for a location.

#### Parameters
- `loc`: See docs on method `current`.

#### Aliases
- `tz`


### `sports_lookup(self, loc: str)`-> [`SportsPoint`](types/types.md)
Get listing of all upcoming sports events for football, cricket and golf. From the behaviour of the WeatherAPI Sports API, parameter `loc` doesn't actually matter but is required anyway.

#### Parameters
- `loc`: See docs on method `current`.

#### Aliases
- `sports`


### `history(self, loc: str, dt: str)` -> [`list[DailyPoint]`](types/types.md)
Get weather history for a location.

#### Parameters
- `loc`: See docs on method `current`.
- `dt`: Datetime string in the format `YYY-MM-DD`. Data starting from this date will be returned.