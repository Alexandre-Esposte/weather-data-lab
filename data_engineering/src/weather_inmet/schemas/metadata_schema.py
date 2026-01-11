from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Metadata:
    region: str
    state_uf: str
    station_name:str
    station_code: str
    latitude: float
    longitude: float
    altitude: float
    fundation_time: datetime

    def to_dict(self):
        return asdict(self)