from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class WeatherCurrentData():
    """
    Immutable data structure representing current weather conditions
    returned by the Open-Meteo API.

    Attributes:
        time (datetime | None): Timestamp of the current weather observation (UTC).
        temperature_2m (float | None): Air temperature at 2 meters above ground (°C).
        relative_humidity_2m (float | None): Relative humidity at 2 meters (%).
        apparent_temperature (float | None): Apparent (feels-like) temperature (°C).
        is_day (bool | None): True if the timestamp corresponds to daytime.
        precipitation (float | None): Total precipitation (mm).
        rain (float | None): Rain precipitation (mm).
        showers (float | None): Shower precipitation (mm).
        snowfall (float | None): Snowfall amount (mm).
        cloud_cover (float | None): Total cloud cover (%).
        pressure_msl (float | None): Mean sea level pressure (hPa).
        surface_pressure (float | None): Surface pressure (hPa).
        wind_speed_10m (float | None): Wind speed at 10 meters (km/h).
        wind_direction_10m (float | None): Wind direction at 10 meters (degrees).
        wind_gusts_10m (float | None): Wind gust speed at 10 meters (km/h).

    Notes:
        This dataclass is frozen (immutable) and intended for read-only usage.
    """

    time: Optional[datetime] = None
    temperature_2m: Optional[float] = None
    relative_humidity_2m: Optional[float] = None
    apparent_temperature: Optional[float] = None
    is_day: Optional[bool] = None
    precipitation: Optional[float] = None
    rain: Optional[float] = None
    showers: Optional[float] = None
    snowfall: Optional[float] = None
    cloud_cover: Optional[float] = None
    pressure_msl: Optional[float] = None
    surface_pressure: Optional[float] = None
    wind_speed_10m: Optional[float] = None
    wind_direction_10m: Optional[float] = None
    wind_gusts_10m: Optional[float] = None
    