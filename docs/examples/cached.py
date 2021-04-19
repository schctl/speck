import os
import speck

from datetime import datetime

def main():
    cl = speck.Client(
        os.environ['WEATHERAPI_TOKEN'],
        use_cache=True # as easy as enabling this flag
    )

    while input('Continue? [y/n] ').lower() in ['yes', 'y']:
        location = input('Location: ')

        try:
            start = datetime.now()
            (current, forecast) = cl.forecast(location)
            stop = datetime.now()
        except speck.errors.WeatherApiError as e:
            print(e.message)

        print('---------------------')
        print(f'Query: {(stop - start).total_seconds()}')
        print(f'Current Temperature: {current.temp_c}°C')
        print(f'Temperature tomorrow: {forecast[0].day.avgtemp_c}°C')
        print('---------------------')

if __name__ == '__main__':
    main()
