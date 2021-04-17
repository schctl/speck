import os
import requests

from datetime import datetime

BASE = "https://api.weatherapi.com/v1"

def main():
    session = requests.Session()

    token = os.environ['WEATHERAPI_TOKEN']

    while input('Continue? [y/n] ').lower() in ['yes', 'y']:
        location = input('Location: ')

        start = datetime.now()
        response = session \
            .get(f'{BASE}/forecast.json?key={token}&q={location}', timeout=(5, 5)) \
            .json()
        stop = datetime.now()

        if 'error' in response:
            if response['error']['code'] == 2006:
                print("Invalid api key provided.")
                break
            elif response['error']['code'] == 2007:
                print("weatherAPI ratelimit reached.")
                continue
            elif response['error']['code'] == 1008:
                print("Provided API key has been disabled.")
                break
            elif response['error']['code'] == 1003:
                print("Location cannot be empty.")
                continue
            elif response['error']['code'] == 1006:
                print("Unknown location.")
                continue

        print('---------------------')
        print(f'Query: {(stop - start).total_seconds()}')
        print(f'Current Temperature: {response["current"]["temp_c"]}°C')
        print(f'Temperature tomorrow: {response["forecast"]["forecastday"][0]["day"]["avgtemp_c"]}°C')
        print('---------------------')

if __name__ == '__main__':
    main()
