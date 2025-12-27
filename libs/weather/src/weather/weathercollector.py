from weatherdata import WeatherCurrentData
from weatherutils import *
from datetime import datetime
import pandas as pd
import requests


def get_currentweather(latitude, longitude)-> WeatherCurrentData:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "snowfall", "showers", "cloud_cover", "pressure_msl", "surface_pressure", "weather_code", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
            "timezone": "auto",
            "timeformat": "unixtime"}


    try:
        res = requests.get(url, headers={"User-Agent": "meu-app"}, params=params)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if verify_request_result(res.status_code):
        data = res.json()
        weather = data['current']
        return WeatherCurrentData(time = datetime.fromtimestamp(weather['time']),
                        temperature_2m = weather['temperature_2m'],
                        relative_humidity_2m = weather['relative_humidity_2m'],
                        apparent_temperature = weather['apparent_temperature'],
                        is_day = weather['is_day'],
                        precipitation = weather['precipitation'],
                        rain = weather['rain'],
                        showers = weather['showers'],
                        snowfall = weather['snowfall'],
                        cloud_cover = weather['cloud_cover'],
                        pressure_msl = weather['pressure_msl'],
                        surface_pressure = weather['surface_pressure'],
                        wind_speed_10m = weather['wind_speed_10m'],
                        wind_direction_10m = weather['wind_direction_10m'],
                        wind_gusts_10m = weather['wind_gusts_10m'])
    else:
        raise requests.exceptions.RequestException(f"Error fetching data | Status code: {res.status_code}")
        

def get_historical_weather(start_date:str, end_date:str, latitude:float, longitude:float):
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "pressure_msl", "surface_pressure", "cloud_cover", "visibility", "wind_speed_10m", "wind_direction_10m", "snowfall", "snow_depth", "wind_gusts_10m"],
        "timezone": "auto",
        "timeformat": "unixtime",
        }
    
    try:
        res = requests.get(url, headers={"User-Agent": "meu-app"}, params=params)
        
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if verify_request_result(res.status_code):
        data = res.json()
        data['hourly']['time'] = [datetime.fromtimestamp(t) for t in data['hourly']['time']]
        return pd.DataFrame(data['hourly'])
    
    else:
        raise requests.exceptions.RequestException(f"Error fetching data | Status code: {res.status_code}")
    


if __name__ == "__main__":
    lat, lon = get_latitude_longitude('BR','RJ','Rio de Janeiro')
    print(lat,lon)
    meteo = get_currentweather(lat, lon)
    hist = get_historical_weather("2025-12-27", "2025-12-27", lat, lon)
    print(meteo, hist)
