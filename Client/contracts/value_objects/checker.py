from Client.contracts.value_objects.checker_type import CheckerType
from Client.contracts.value_objects.possible_move import PossibleMove


class Checker:
    def __init__(self, checker_num: int, your_checker: bool, x: int, y: int, checker_type: CheckerType,
                 possible_moves: list[PossibleMove]):
        self.checker_num: int = checker_num
        self.your_checker = your_checker
        self.x: int = x
        self.y: int = y
        self.checker_type: CheckerType = checker_type
        self.possible_moves: list[PossibleMove] = possible_moves
    
    def __repr__(self):
        # TODO: mayby add checker_num, your_checker and possible_moves
        return f"Checker(x={self.x}, y={self.y}, color={self.checker_type.name})"
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, Checker):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return all([
            self.checker_num == other.checker_num,
            self.your_checker == other.your_checker,
            self.x == other.x,
            self.y == other.y,
            self.checker_type == other.checker_type,
            # self.possible_moves == other.possible_moves,  # TODO: fix it
        ])

    @staticmethod
    def from_json(obj):
        checker_num, your_checker, x, y, checker_type = obj['checker_num'], obj['your_checker'], obj['x'], obj['y'],\
                                                        CheckerType(obj['checker_type'])
        possible_moves = []
        if 'possible_moves' in obj:
            possible_moves = [PossibleMove.from_json(move_json) for move_json in obj['possible_moves']]
        return Checker(checker_num, your_checker, x, y, checker_type, possible_moves)
