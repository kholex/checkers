"""This module describes part of contracts with server about checker info."""
from contracts.value_objects.checker_type import CheckerType
from contracts.value_objects.possible_move import PossibleMove


class Checker:
    """Info about checker and possible for its moves."""

    def __init__(self, checker_num: int, your_checker: bool, x: int, y: int, checker_type: CheckerType,
                 possible_moves: list[PossibleMove]):
        """Initialize checker info."""
        self.checker_num: int = checker_num
        self.your_checker = your_checker
        self.x: int = x
        self.y: int = y
        self.checker_type: CheckerType = checker_type
        self.possible_moves: list[PossibleMove] = possible_moves

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        checker_num, your_checker, x, y, checker_type = obj['checker_num'], obj['your_checker'], obj['x'], obj['y'],\
                                                        CheckerType(obj['checker_type'])
        possible_moves = []
        if 'possible_moves' in obj:
            possible_moves = [PossibleMove.from_json(move_json) for move_json in obj['possible_moves']]
        return Checker(checker_num, your_checker, x, y, checker_type, possible_moves)
