from dataclasses import dataclass
from datetime import datetime

class Resource:
    def __post_init__(self):
        for attr_name, data_type in self.__annotations__.items():
            if data_type is datetime and isinstance(getattr(self, attr_name), str):
                setattr(self, attr_name, datetime.fromisoformat(getattr(self, attr_name)))

@dataclass
class ResponseEnvelope(Resource):
    StatusCode: int
    Message: str
    ExecutionTime: int = None
    ResponseData: list = None
