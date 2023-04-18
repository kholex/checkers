import json


class AuthorizeResponse:
    def __init__(self, result: bool):
        self.type = "authorize_response"
        self.result = result

    @staticmethod
    def from_json(obj):
        return AuthorizeResponse(obj['result'])

    def to_json(self):
        return json.dumps(self.__dict__)
