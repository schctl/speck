Speck
-----
Speck is a frontend, and minimal API wrapper for [weatherAPI.com](https://www.weatherapi.com/). See the [README](../README.md) for more info.

## Examples

#### Basic Client

```py
import os
import speck

from speck.waw.client import Client

def main():
    cl = Client(
        os.environ['WEATHERAPI_TOKEN'] # Get from https://www.weatherapi.com/my/
    )

    while input('Continue? [y/n] ').lower() in ['yes', 'y']:
        location = input('Location: ')

        current = cl.current(location)
        forecast = cl.forecast(location)

        print('---------------------')
        print(f'Current Temperature: {current.temp_c}°C')
        print(f'Temperature tomorrow: {forecast[0].day.avgtemp_c}°C')
        print('---------------------')

if __name__ == '__main__':
    main()
```

## API Reference

### Packages
- [cache](cache/cache.md)
- [waw](waw/waw.md)
- [ext](ext/ext.md)
