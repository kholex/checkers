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
    
    def __repr__(self):
        # TODO: mayby add new_type and remove_checker_num
        return f"PossibleMove(x={self.x}, y={self.y})"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, PossibleMove):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return all([
            self.x == other.x,
            self.y == other.y,
            self.new_type == other.new_type,
            self.remove_checker_num == other.remove_checker_num,
        ])

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        return PossibleMove(obj['x'], obj['y'],
                            obj['new_type'] if 'new_type' in obj else None,
                            obj['remove_checker_num'] if 'remove_checker_num' in obj else None)
