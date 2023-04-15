from CheckerType import CheckerType
from PossibleMove import PossibleMove


class Checker:
    def __init__(self, x: int, y: int, checker_type: CheckerType, possible_moves: list[PossibleMove]):
        self.x: int = x
        self.y: int = y
        self.checker_type: CheckerType = checker_type
        self.possible_moves: list[PossibleMove] = possible_moves
