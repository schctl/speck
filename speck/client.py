"""
WeatherAPI client implementation.
Use this to make requests to weatherapi.com.
"""

import os
import json

from datetime import datetime as dt

import requests

from speck.cache import CacheManager

from . import errors
from . import types

__all__ = [
    'Client'
]

class _DummyCache:
    """
    Dummy cache type so checks don't have to be performed
    if `Client` has opt out of cache.
    """

    def __init__(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        pass

    def dump(self, *args, **kwargs):
        pass

    def cleanup(self, *args, **kwargs):
        pass

class Client:
    """
    Represents a connection to weatherapi.com.
    Use this class to interact with the weatherapi API.
    """

    BASE = "https://api.weatherapi.com/v1"

    def __init__(self, token, use_cache=False, cache_path='.cache'):
        self.token = token
        self.session = requests.Session()

        if use_cache:
            self.cache = CacheManager(cache_path)
        else:
            self.cache = _DummyCache()

        # This looks for the cities list file
        with open(
            os.path.join(os.path.dirname(__file__), 'etc/cities_p.json'),
            'r', encoding='utf-8'
        ) as f:
            self.cities = json.loads(f.read())

    @staticmethod
    def __is_error_code(response):
        """
        Convert weatherapi.com provided error code to Error Type.

        :param response: The raw weatherapi.com response.
        """
        if "error" in response:
            code = response['error']['code']
            message = response['error']['message']

            # These are hardcoded
            if code == 1002:
                return errors.NoApiKey(message, code)
            elif code == 1003:
                return errors.QueryNotProvided(message, code)
            elif code == 1005:
                return errors.InvalidRequestUrl(message, code)
            elif code == 1006:
                return errors.InvalidLocation(message, code)
            elif code == 2006:
                return errors.InvalidApiKey(message, code)
            elif code == 2007:
                return errors.QuotaExceeded(message, code)
            elif code == 2008:
                return errors.ApiKeyDisabled(message, code)
            elif code == 9999:
                return errors.InternalError(message, code)
            else:
                return errors.WeatherApiError(message, code)

        return

    def __make_request(self, endpoint, parameters):
        """Private method to make a request to ``weatherapi.com``."""
        try:
            # Does the acutal request
            return self.session.get(f"{self.BASE}/{endpoint}{parameters}").json()
        except Exception as e:
            raise errors.InternalError(f"Unable to fetch data at this time: {e.__traceback__}", 9999)

    def find_city(self, loc):
        """
        Try to find a city with a match from a known list of locations.
        This method is highly unlikely to be used frequently, since weatherAPI tries
        to interpret location names even if incorrect, but is provided anyway.
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        return [ # Generates a list of city names containing the string `loc`
            i for i in self.cities if loc.lower() in i['name'].lower()
        ]

    def current(self, loc):
        """
        Get current weather conditions in a location.

        :param loc: Query location to find data for. It could be following:\n
             - **Latitude and Longitude (Decimal degree)**. *e.g:'48.8567,2.3508'*,\n
             - **city name** *e.g: 'Paris'*,\n
             - **US zip** *e.g: '10001'*,\n
             - **UK postcode** *e.g: 'SW1'*,\n
             - **Canada postal code** *e.g: 'G2J'*,\n
             - **metar:<metar code>** *e.g: 'metar:EGLL'*,\n
             - **iata:<3 digit airport code>** *e.g: 'iata:DXB'*,\n
             - **auto:ip IP lookup** *e.g: 'auto:ip'*,\n
             - **IP address (IPv4 and IPv6 supported)** *e.g: '100.0.0.1*'
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        mode = f"current-{loc}-now-{str(dt.now())[:15].replace(' ', '-')}"

        n = self.cache.read(mode)
        if n:
            # If cache exists (not None), it will be read and an `HourlyPoint` object will be returned
            return n

        response = self.__make_request('current.json', f'?key={self.token}&q={loc}')

        e = Client.__is_error_code(response)
        if e:
            raise e # We're not going to handle the error here, so anyone using the function can do it themselves

        data = types.HourlyPoint.from_raw(response["location"], response["current"]) # Creates the `HourlyPoint` object

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*') # Discard any old cache
        self.cache.dump(mode, data) # Writes cache

        return data

        ## The same pattern is followed for all other API methods implemented.

    def forecast(self, loc, days=3):
        """
        Get weather forecast for a location.

        :param loc: See docs on method ``current``.
        :param days: Number of days to restrict the forecast for.
            WeatherAPI allows up to 10 days, but it in practice the maximum is 3.
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        mode = f"forecast-{loc}-now-{str(dt.now()).split()[0]}-{days}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('forecast.json', f'?key={self.token}&q={loc}&days={min(days, 10)}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        data = [
            types.DailyPoint(response["location"], i["day"], i["astro"], i["hour"])
            for i in response["forecast"]["forecastday"]
        ]

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data

    def astronomy(self, loc):
        """
        Get astronomy information for a location.

        :param loc: See docs on method ``current``.
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        mode = f"astro-{loc}-now-{str(dt.now()).split()[0]}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('astronomy.json', f'?key={self.token}&q={loc}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        data = types.AstroPoint.from_raw(response["location"], response["astronomy"]["astro"])

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data

    def ip_lookup(self, ip):
        """
        Get information for an IP address.

        :param ip: IPv6 or IPv4 string.
        """

        if ip == '':
            raise errors.QueryNotProvided('IP cannot be empty.', 0)

        mode = f"iplookup-{ip}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('ip.json', f'?key={self.token}&q={ip}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        data = types.IpPoint.from_raw(response)

        # self.cache.cleanup(mode) # We don't need this here
        self.cache.dump(mode, data)

        return data

    def search(self, loc):
        """
        Get a list of location objects based on query parameter.

        :param loc: See docs on method ``current``.
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        mode = f"search-{loc}"

        n = self.cache.read(mode)

        if n:
            return n

        response = self.__make_request('search.json', f'?key={self.token}&q={loc}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        data = [
            types.Location.from_raw(i)
            for i in response
        ]

        # self.cache.cleanup(mode) # We don't need this here
        self.cache.dump(mode, data)

        return data

    def timezone_info(self, loc):
        """
        Get timezone and associated information for a location.

        :param loc: See docs on method ``current``.
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        # No cache

        response = self.__make_request('timezone.json', f'?key={self.token}&q={loc}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        return types.Location.from_raw(response["location"])

    def sports_lookup(self, loc):
        """
        Get listing of all upcoming sports events for football,
        cricket and golf. From the behaviour of the WeatherAPI Sports API,
        parameter `loc` doesn't actually matter but is required anyway.

        :param loc: See docs on method ``current``.
        """
        mode = f"sports-{loc}-now-{str(dt.now()).split()[0]}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('sports.json', f'?key={self.token}&q={loc}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        data = types.SportsPoint.from_raw(response)

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data

    def history(self, loc, dt):
        """
        Get weather history for a location.

        :param loc: See docs on method ``current``.
        :param dt: Datetime string in the format `YYY-MM-DD`.
            Data starting from this date will be returned.
        """

        if loc == '':
            raise errors.QueryNotProvided('Location cannot be empty.', 0)

        mode = f"history-{loc}-now-{str(dt.now()).split()[0]}-{dt}"

        n = self.cache.read(mode)
        if n:
            return n


        response = self.__make_request('history.json', f'?key={self.token}&q={loc}&dt={min(dt, 10)}')

        e = Client.__is_error_code(response)
        if e:
            raise e

        data = [
            types.DailyPoint(n["location"], i["day"], i["astro"], i["hour"])
            for i in n["forecast"]["forecastday"]
        ]

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data # `forecast->forecastday` is a list of all daily forecasts

    # Aliases ---------------------------------------

    def astro(self, *args, **kwargs):
        """Alias for ``astronomy``."""
        return self.astronomy(*args, **kwargs)

    def ip(self, *args, **kwargs):
        """Alias for ``ip_lookup``."""
        return self.ip_lookup(*args, **kwargs)

    def tz(self, *args, **kwargs):
        """Alias for ``timezone_info``."""
        return self.timezone_info(*args, **kwargs)

    def sports(self, *args, **kwargs):
        """Alias for ``sports_lookup``."""
        return self.sports_lookup(*args, **kwargs)
