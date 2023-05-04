"""This module describes part of contracts with server about checker info."""
from .checker_type import CheckerType
from .possible_move import PossibleMove


class Checker:
    """Info about checker and possible for its moves."""

    def __init__(
        self,
        checker_num: int,
        your_checker: bool,
        x: int,
        y: int,
        checker_type: CheckerType,
        possible_moves: list[PossibleMove],
    ):
        """Initialize checker info."""
        self.checker_num: int = checker_num
        self.your_checker = your_checker
        self.x: int = x
        self.y: int = y
        self.checker_type: CheckerType = checker_type
        self.possible_moves: list[PossibleMove] = possible_moves

    def __repr__(self):
        """Pretty print."""
        return f"Checker(num={self.checker_num}, your_checker={self.your_checker}, x={self.x}, y={self.y}, color={self.checker_type.name}, possible_moves={self.possible_moves})"

    def __str__(self):
        """Pretty print."""
        return self.__repr__()

    def __eq__(self, other):
        """Compare Checkers."""
        if not isinstance(other, Checker):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return all(
            [
                self.checker_num == other.checker_num,
                self.your_checker == other.your_checker,
                self.x == other.x,
                self.y == other.y,
                self.checker_type == other.checker_type,
                len(self.possible_moves) == len(other.possible_moves),
                all(
                    [
                        self.possible_moves[i] == other.possible_moves[i]
                        for i in range(len(self.possible_moves))
                    ]
                ),
            ]
        )

    def to_json(self):
        """Object to json."""
        return {
            "checker_num": self.checker_num,
            "your_checker": self.your_checker,
            "x": self.x,
            "y": self.y,
            "checker_type": self.checker_type.value,
            "possible_moves": [move.to_json() for move in self.possible_moves],
        }

    @staticmethod
    def from_json(obj):
        """Deserialize object from json."""
        checker_num, your_checker = obj["checker_num"], obj["your_checker"]
        x, y, checker_type = obj["x"], obj["y"], CheckerType(obj["checker_type"])
        possible_moves = []
        if "possible_moves" in obj:
            possible_moves = [
                PossibleMove.from_json(move_json) for move_json in obj["possible_moves"]
            ]
        return Checker(checker_num, your_checker, x, y, checker_type, possible_moves)
