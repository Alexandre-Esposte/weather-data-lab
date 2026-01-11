from sqlalchemy import Column, String, Float, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class Stations(Base):

    __tablename__ = 'stations'

    region = Column(String(2), nullable=False)
    state_uf = Column(String(2), nullable=False)
    station_name = Column(String, nullable=False)
    station_code = Column(String, nullable=False, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)
    fundation_time = Column(Date, nullable=False)
    
    # Relacionamento 1 -> N
    weather_data = relationship(
        "WeatherData",
        back_populates="station",
        cascade="all, delete-orphan")



class WeatherData(Base):

    __tablename__ = 'weather_data'
    
    dt = Column(DateTime, nullable=False, primary_key=True)
    station_code = Column(String,ForeignKey('stations.station_code'),nullable=False, primary_key=True)
    total_precipitation = Column(Float)
    air_pressure = Column(Float)
    global_radiation = Column(Float)
    air_temperature = Column(Float)
    dew_point_temperature = Column(Float)
    relative_humidity = Column(Float)
    wind_direction = Column(Float)
    max_wind_speed = Column(Float)
    wind_speed = Column(Float)

    # Relacionamento N -> 1
    station = relationship(
        "Stations",
        back_populates="weather_data")



       