import json


class AuthorizeCommand:
    def __init__(self, login: str):
        self.type = "authorize_command"
        self.login = login

    @staticmethod
    def from_json(obj):
        return AuthorizeCommand(obj['login'])

    def to_json(self):
        return json.dumps(self.__dict__)
