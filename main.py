import requests
from datetime import datetime, timezone, timedelta
import time
import math


def main():
    threshold = 52  # degrees Fahrenheit

    forecast = get_forecast()
    cold_data_points = get_cold_data_points(forecast, threshold)
    report(cold_data_points, threshold)


def get_cold_data_points(forecast, threshold):
    for d in forecast['list']:
        temp_in_kelvin = float(d['main']['temp_min'])
        if math.floor(k_to_f(temp_in_kelvin)) <= math.ceil(threshold):
            yield d


def report(cold_data_points, threshold):
    count = 0
    cold_start_time = None
    for dp in cold_data_points:
        if count == 0:
            print(f"The following times are colder than your threshold of {threshold}˚F:")
        count += 1
        temp = round(k_to_f(dp['main']['temp_min']))
        formatted_time = utc_to_local(dp['dt']).strftime("%A at %-I %p")
        if cold_start_time is None:
            cold_start_time = formatted_time
        print(f"  {formatted_time}: {temp}˚F")
    if count > 0:
        print(f"You should bring your plants in before {cold_start_time}")
    else:
        print(f"The forecast is warmer than your threshold of {threshold}˚F, your plants are fine outside!")


def get_forecast():
    return requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?q=houston&appid=c1cb26a42f903e05b5739fef6187564f').json()


def utc_to_local(utc_dt):
    tz = timezone(timedelta(hours=-6))
    return datetime.fromtimestamp(utc_dt).replace(tzinfo=timezone.utc).astimezone(tz=tz)


def k_to_f(k):
    return ((k - 273.15) * (9.0 / 5)) + 32


def round(x):
    return int(x)


if __name__ == '__main__':
    main()
