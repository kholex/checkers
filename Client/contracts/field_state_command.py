import json
from contracts.value_objects.checker import Checker


class FieldStateCommand:
    def __init__(self, checkers: list[Checker]):
        self.type = "field_state_command"
        self.checkers = checkers

    @staticmethod
    def from_json(obj):
        checkers = [Checker.from_json(checker_json) for checker_json in obj["checkers"]]
        return FieldStateCommand(checkers)

    def to_json(self):
        return json.dumps(self.__dict__)
