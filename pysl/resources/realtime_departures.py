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
    GroupOfLine: str
    StopAreaName: str
    StopAreaNumber: int
    LineNumber: str = None
    Destination: str = None
    JourneyDirection: int = None
    StopPointDesignation: str = None
    StopPointNumber: int = None
    TimeTabledDateTime: datetime = None
    ExpectedDateTime: datetime = None
    DisplayTime: str = None
    JourneyNumber: int = None
    Deviations: list = None
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
