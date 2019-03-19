from dataclasses import dataclass

class Resource:
    pass

@dataclass
class ResponseEnvelope(Resource):
    StatusCode: int
    Message: str
    ExecutionTime: int
    ResponseData: list
