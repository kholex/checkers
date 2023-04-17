from contracts.value_objects.checker_type import CheckerType
from contracts.value_objects.possible_move import PossibleMove


class Checker:
    def __init__(self, checker_num: int, your_checker: bool, x: int, y: int, checker_type: CheckerType, possible_moves: list[PossibleMove]):
        self.your_checker = your_checker
        self.checker_num: int = checker_num
        self.x: int = x
        self.y: int = y
        self.checker_type: CheckerType = checker_type
        self.possible_moves: list[PossibleMove] = possible_moves

    @staticmethod
    def checker_decoder(obj):
        checker_num, your_checker, x, y, checker_type = obj['checker_num'], obj['your_checker'], obj['x'], obj['y'],\
                                                        CheckerType(obj['checker_type'])
        possible_moves = []
        if 'possible_moves' in obj:
            possible_moves = [PossibleMove.possible_move_decoder(move_json) for move_json in obj['possible_moves']]
        return Checker(checker_num, your_checker, x, y, checker_type, possible_moves)
