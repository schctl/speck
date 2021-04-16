import os
import speck

from speck import errors

from datetime import datetime

def main():
    cl = speck.Client(
        os.environ['WEATHERAPI_TOKEN'], # Get from https://www.weatherapi.com/my/
        use_cache=True
    )

    while input('Continue? [y/n] ').lower() in ['yes', 'y']:
        location = input('Location: ')

        try:
            start = datetime.now()
            (current, forecast) = cl.forecast(location)
            stop = datetime.now()

        except errors.InvalidApiKey:
            print("Invalid api key provided.")
            break
        except errors.QuotaExceeded:
            print("weatherAPI ratelimit reached.")
            continue
        except errors.ApiKeyDisabled:
            print("Provided API key has been disabled.")
            break
        except errors.QueryNotProvided:
            print("Location cannot be empty.")
            continue
        except errors.InvalidLocation:
            print("Unknown location.")
            continue

        print('---------------------')
        print(f'Query: {(stop - start).total_seconds()}')
        print(f'Current Temperature: {current.temp_c}°C')
        print(f'Temperature tomorrow: {forecast[0].day.avgtemp_c}°C')
        print('---------------------')

if __name__ == '__main__':
    main()
