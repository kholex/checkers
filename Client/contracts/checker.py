import json

from contracts.checker_type import CheckerType
from contracts.possible_move import PossibleMove


class Checker:
    def __init__(self, checker_num: int, x: int, y: int, checker_type: CheckerType, possible_moves: list[PossibleMove]):
        self.checker_num: int = checker_num
        self.x: int = x
        self.y: int = y
        self.checker_type: CheckerType = checker_type
        self.possible_moves: list[PossibleMove] = possible_moves

    @staticmethod
    def checker_decoder(obj):
        possible_moves = [PossibleMove.possible_move_decoder(move_json) for move_json in obj['possible_moves']]
        return Checker(obj['checker_num'], obj['x'], obj['y'], CheckerType(obj['checker_type']), possible_moves)
