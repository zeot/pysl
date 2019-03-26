from dataclasses import dataclass
from datetime import datetime

class Resource:
    def __post_init__(self):
        for attr_name, data_type in self.__annotations__.items():
            attr = getattr(self, attr_name)
            if attr is None:
                continue
            if data_type is datetime and isinstance(attr, str):
                setattr(self, attr_name, datetime.fromisoformat(attr))
            elif data_type in {int, str, bool, float} and not isinstance(attr, data_type):
                setattr(self, attr_name, data_type(attr))

@dataclass
class ResponseEnvelope(Resource):
    StatusCode: int
    Message: str
    ExecutionTime: int = None
    ResponseData: list = None
