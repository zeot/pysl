from dataclasses import dataclass
from datetime import datetime
from pysl.resources import general

@dataclass
class RealtimeDepartures(general.Resource):
    LatestUpdate: datetime
    DataAge: int
    Buses: list
    Metros: list
    Trains: list
    Trams: list
    Ships: list
    StopPointDeviations: list

@dataclass
class Transport(general.Resource):
    TransportMode: str
    LineNumber: str
    Destination: str
    JourneyDirection: int
    GroupofLine: str
    StopAreaName: str
    StopAreaNumber: int
    StopPointDesignation: str
    TimeTabledDateTime: datetime
    ExpectedDateTime: datetime
    DisplayTime: str
    JourneyNumber: int
    Deviations: list
    SecondaryDestinationName: str = None

@dataclass
class Deviation(general.Resource):
    Consequence: str
    ImportanceLeve: int
    Text: str

@dataclass
class StopInfo(general.Resource):
    GroupOfLine: str
    StopAreaName: str
    StopAreaNumber: int
    TransportMode: str

@dataclass
class StopPointDeviations(general.Resource):
    StopInfo: StopInfo
    Deviation: Deviation

__all__ = [RealtimeDepartures, Transport, Deviation, StopPointDeviations, StopInfo]
