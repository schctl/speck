import os
import json
import requests

from datetime import datetime as dt

from cache import Cache

from . import errors
from . import types

class __DummyCache:
    def __init__(*args, **kwargs):
        pass

    def read(*args, **kwargs):
        pass

    def dump(*args, **kwargs):
        pass

    def cleanup(*args, **kwargs):
        pass

class Client:
    """weatherAPI client."""

    BASE = "https://api.weatherapi.com/v1"

    def __init__(self, token, use_cache = False, cache_path = '.cache'):
        self.token = token
        self.session = requests.Session()

        if use_cache:
            self.cache = Cache(cache_path)
        else:
            self.cache = __DummyCache()

        print(
            f'{os.path.abspath(os.path.dirname(__file__))}/../etc/cities_p.json'
        )

        # This looks for the cities list file
        with open(
            f'{os.path.abspath(os.path.dirname(__file__))}/../etc/cities_p.json',
            'r', encoding='utf-8'
        ) as f:
            self.cities = json.loads(f.read())

    @staticmethod
    def __error_code_to_error(response):
        """
        Convert weatherapi.com provided error code to Error Type.

        * Parameter `response` should be the raw weatherapi.com response.
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
        """Private method to make a request to `weatherapi.com`."""
        try:
            return self.session.get(f"{self.BASE}/{endpoint}{parameters}").json() # Does the acutal request
        except Exception as e:
            raise errors.InternalError(f"Unable to fetch data at this time: {e.__traceback__}", 9999)

    def find_city(self, loc):
        """Returns an array of city names and coordinates containing a search pattern."""
        return [ # Generates a list of city names containing the string `loc`
            i for i in self.cities if loc.lower() in i['name'].lower()
        ]

    def current(self, loc):
        """
        Get current weather conditions in a location.

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back. It could be following:

                    - Latitude and Longitude (Decimal degree). e.g.:'48.8567,2.3508'
                    - city name e.g.: 'Paris'
                    - US zip e.g.: '10001'
                    - UK postcode e.g: 'SW1'
                    - Canada postal code e.g: 'G2J'
                    - metar:<metar code> e.g: 'metar:EGLL'
                    - iata:<3 digit airport code> e.g: 'iata:DXB'
                    - auto:ip IP lookup e.g: 'auto:ip'
                    - IP address (IPv4 and IPv6 supported) e.g: '100.0.0.1'
        """
        mode = f"current-{loc}-now-{str(dt.now())[:15]}"

        n = self.cache.read(mode)
        if n:
            # If cache exists (not None), it will be read and an `HourlyPoint` object will be returned
            return n

        response = self.__make_request('current.json', f'?key={self.token}&q={loc}')

        e = Client.__error_code_to_error(response)
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

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back. See docs on method `current` for more info.

        * **days:** Number of days to forecast for. Maximum is 10.
        """
        mode = f"forecast-{loc}-now-{str(dt.now()).split()[0]}-{days}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('forecast.json', f'?key={self.token}&q={loc}&days={min(days, 10)}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        data = list(
            map(
                lambda i: types.DailyPoint(response["location"], i["day"], i["astro"], i["hour"]),
                response["forecast"]["forecastday"]
            )
        )

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data

    def astronomy(self, loc):
        """
        Get current astronomy information in a location.

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back. See docs on method `current` for more info.
        """
        mode = f"astro-{loc}-now-{str(dt.now()).split()[0]}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('astronomy.json', f'?key={self.token}&q={loc}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        data = types.AstroPoint.from_raw(response["location"], response["astronomy"]["astro"])

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data

    def ip_lookup(self, ip):
        """
        Get information for an IP address.

        Paramters
        ---------
        * **ip:** IP address string
        """
        mode = f"iplookup-{ip}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('ip.json', f'?key={self.token}&q={ip}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        data = types.IpPoint.from_raw(response)

        # self.cache.cleanup(mode) # We don't need this here
        self.cache.dump(mode, data)

        return data

    def search(self, loc):
        """
        Get an array of location objects based on query parameter.

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back. See docs on method `current` for more info.
        """
        mode = f"search-{loc}"

        n = self.cache.read(mode)

        if n:
            return n

        response = self.__make_request('search.json', f'?key={self.token}&q={loc}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        data = list(map(lambda i: types.Location.from_raw(i), response))

        # self.cache.cleanup(mode) # We don't need this here
        self.cache.dump(mode, data)

        return data

    def timezone_info(self, loc):
        """
        Get timezone information for a location.

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back.
                   See docs on method `current` for more info.
        """
        # No cache

        response = self.__make_request('timezone.json', f'?key={self.token}&q={loc}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        return types.Location.from_raw(response["location"])

    def sports_lookup(self, loc):
        """
        Get listing of all upcoming sports events for football, cricket and golf.
        Judging from the behaviour of the WeatherAPI Sports API, parameter `loc` doesn't actually matter but is required anyway.

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back. See docs on method `current` for more info.
        """
        mode = f"sports-{loc}-now-{str(dt.now()).split()[0]}"

        n = self.cache.read(mode)
        if n:
            return n

        response = self.__make_request('sports.json', f'?key={self.token}&q={loc}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        data = types.SportsPoint.from_raw(response)

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data

    def history(self, loc, dt):
        """
        Get weather history for a location.

        Paramters
        ---------
        * **loc:** Query parameter based on which data is sent back. See docs on method `current` for more info.

        * **dt:** Restrict number of days of history to fetch. Should be on or after 2015-01-01.

        # WARNING: This method has not been tested.
        """
        mode = f"history-{loc}-now-{str(dt.now()).split()[0]}-{dt}"

        n = self.cache.read(mode)
        if n:
            return n


        response = self.__make_request('history.json', f'?key={self.token}&q={loc}&dt={min(dt, 10)}')

        e = Client.__error_code_to_error(response)
        if e:
            raise e

        data = list(
            map(
                lambda i: types.DailyPoint(n["location"], i["day"], i["astro"], i["hour"]),
                n["forecast"]["forecastday"]
            )
        )

        self.cache.cleanup(mode.split('-now-')[0] + '-now-*')
        self.cache.dump(mode, data)

        return data # `forecast->forecastday` is a list of all daily forecasts

    # Aliases ---------------------------------------

    def astro(self, *args, **kwargs):
        """Alias for `astronomy`."""
        return self.astronomy(*args, **kwargs)

    def ip(self, *args, **kwargs):
        """Alias for `ip_lookup`."""
        return self.ip_lookup(*args, **kwargs)

    def tz(self, *args, **kwargs):
        """Alias for `timezone_info`."""
        return self.timezone_info(*args, **kwargs)

    def sports(self, *args, **kwargs):
        """Alias for `sports_lookup`."""
        return self.sports_lookup(*args, **kwargs)
