"""This module describes part of contracts with server about authorize process."""
import json


class AuthorizeResponse:
    """Response for authorize command from server."""

    def __init__(self, result: bool):
        """Initialize authorize response."""
        self.type = "authorize_response"
        self.result = result

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        return AuthorizeResponse(obj["result"])

    def to_json(self):
        """Serialize object to json."""
        return json.dumps(self.__dict__)
