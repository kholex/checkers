"""This module describes part of contracts with server about authorize process."""
import json


class AuthorizeCommand:
    """Command for authorize in server."""

    def __init__(self, login: str):
        """Initialize command for authorize."""
        self.type = "authorize_command"
        self.login = login

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        return AuthorizeCommand(obj["login"])

    def to_json(self):
        """Serialize object to json."""
        return json.dumps(self.__dict__)
