from weatherdata import WeatherData
from typing import Self
import requests


class CurrentWeather():

    def _verify_request_result(self,status_code: int = None):
        if status_code == 200:
            return True
        else:
            return False


    def get_latitude_longitude(self,country_code: str=None, state_code: str=None, city_name: str = None) -> tuple[float, float]:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": f"{city_name} {state_code} {country_code}",
            "format": "json",
            "limit": 1
        }
        res = requests.get(url, headers={"User-Agent": "meu-app"}, params=params)

        if self._verify_request_result(res.status_code):
            data = res.json()
            return float(data[0]["lat"]), float(data[0]["lon"])
        
        else:
            raise Exception('Deu erro')

    def get_weather(self, latitude, longitude)-> WeatherData:

        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&timezone=auto"

        res = requests.get(url, headers={"User-Agent": "meu-app"})
        data = res.json()
        
        weather = data['current']

        return WeatherData(time = weather['time'],
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
        

if __name__ == "__main__":
    data = CurrentWeather()
    lat, lon = data.get_latitude_longitude('BR','RJ','Volta Redonda')
    print(lat,lon)
    meteo = data.get_weather(lat, lon)
    print(meteo, type(meteo), type(meteo.time))
