from dataclasses import dataclass
from pysl.resources import general

@dataclass
class Site(general.Resource):
    Name: str
    SiteId: int
    Type: str
    X: str
    Y: str

__all__ = [Site]
