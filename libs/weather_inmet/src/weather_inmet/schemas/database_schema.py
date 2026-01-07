from sqlalchemy import Column, String, Float, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stations(Base):

    __tablename__ = 'stations'

    station_code = Column(String, nullable=False, primary_key=True)
    station_name = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, nullable=False)

    state_uf = Column(String(2), nullable=False)
    region = Column(String(2), nullable=False)

    data_fundation = Column(Date, nullable=False)

       