from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class WeatherData():

    time: datetime = None,
    temperature_2m: float = None,
    relative_humidity_2m: float = None,
    apparent_temperature: float = None,
    is_day: bool =  None,
    precipitation: float = None ,
    rain: float = None ,
    showers: float = None,
    snowfall: float = None,
    cloud_cover: float = None,
    pressure_msl: float = None,
    surface_pressure: float = None,
    wind_speed_10m: float = None,
    wind_direction_10m: float = None,
    wind_gusts_10m: float = None
    