from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class WeatherCurrentData():

    time: Optional[datetime] = None,
    temperature_2m: Optional[float] = None,
    relative_humidity_2m: Optional[float] = None,
    apparent_temperature: Optional[float] = None,
    is_day: Optional[bool] = None,
    precipitation: Optional[float] = None,
    rain: Optional[float] = None,
    showers: Optional[float] = None,
    snowfall: Optional[float] = None,
    cloud_cover: Optional[float] = None,
    pressure_msl: Optional[float] = None,
    surface_pressure: Optional[float] = None,
    wind_speed_10m: Optional[float] = None,
    wind_direction_10m: Optional[float] = None,
    wind_gusts_10m: Optional[float] = None
    