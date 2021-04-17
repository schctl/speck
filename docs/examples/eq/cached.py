import os
import zlib
import pickle
from pathlib import Path

from datetime import datetime

import requests

BASE = "https://api.weatherapi.com/v1"

def display_details(response, query):
    if 'error' in response:
        if response['error']['code'] == 2006:
            print("Invalid api key provided.")
            return
        elif response['error']['code'] == 2007:
            print("weatherAPI ratelimit reached.")
            return
        elif response['error']['code'] == 1008:
            print("Provided API key has been disabled.")
            return
        elif response['error']['code'] == 1003:
            print("Location cannot be empty.")
            return
        elif response['error']['code'] == 1006:
            print("Unknown location.")
            return

    print('---------------------')
    print(f'Query: {query}')
    print(f'Current Temperature: {response["current"]["temp_c"]}°C')
    print(f'Temperature tomorrow: {response["forecast"]["forecastday"][0]["day"]["avgtemp_c"]}°C')
    print('---------------------')

def main():
    session = requests.Session()

    token = os.environ['WEATHERAPI_TOKEN']

    Path('.cache').mkdir(parents=True, exist_ok=True)

    while input('Continue? [y/n] ').lower() in ['yes', 'y']:
        location = input('Location: ')

        data = None

        for i in os.listdir('.cache'):
            if i == f'{location.lower()}-{datetime.now().strftime("%Y-%m-%d %H-%M")[:-1]}.dat':
                with open(i, 'rb') as f:
                    data = pickle.loads(zlib.decompress(pickle.load(f)))

        if not data:
            start = datetime.now()
            data = session \
                .get(f'{BASE}/forecast.json?key={token}&q={location}', timeout=(5, 5)) \
                .json()
            stop = datetime.now()

            with open(f'.cache/{location.lower()}-{datetime.now().strftime("%Y-%m-%d %H-%M")[:-1]}.dat', 'wb') as f:
                pickle.dump(zlib.compress(pickle.dumps(data)), f)

        display_details(data, (stop - start).total_seconds())

if __name__ == '__main__':
    main()
