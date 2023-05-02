"""This module describes part of contracts with server about field state."""
import json
from .value_objects.checker import Checker


class FieldStateCommand:
    """Command from server with info about current state of field."""

    def __init__(self, checkers: list[Checker]):
        """Initialize field state."""
        self.type = "field_state_command"
        self.checkers = checkers

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        checkers = [Checker.from_json(checker_json) for checker_json in obj["checkers"]]
        return FieldStateCommand(checkers)

    def to_json(self):
        """Serialize object to json."""
        return json.dumps(self.__dict__)
