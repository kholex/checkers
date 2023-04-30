"""This module describes part of contracts with server about possible checkers moves."""
from .checker_type import CheckerType


class PossibleMove:
    """Possible move for checkers."""

    def __init__(self, x: int, y: int, new_type: CheckerType = None, remove_checker_num: int = None):
        """Initialize possible move."""
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        return PossibleMove(obj['x'], obj['y'],
                            obj['new_type'] if 'new_type' in obj else None,
                            obj['remove_checker_num'] if 'remove_checker_num' in obj else None)
