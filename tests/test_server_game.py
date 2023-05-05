import unittest

from Client.contracts.value_objects.checker import Checker
from Client.contracts.value_objects.checker_type import CheckerType
from Client.contracts.value_objects.possible_move import PossibleMove
from Server.field_state import FieldState


class TestServerUtils(unittest.TestCase):
    def test_field_state(self):

        game_state = FieldState()

        checkers_true = [
            Checker(checker_num=0, your_checker=False, x=1, y=0, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=1, your_checker=False, x=3, y=0, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=2, your_checker=False, x=5, y=0, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=3, your_checker=False, x=7, y=0, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=4, your_checker=False, x=0, y=1, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=5, your_checker=False, x=2, y=1, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=6, your_checker=False, x=4, y=1, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=7, your_checker=False, x=6, y=1, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=8, your_checker=False, x=1, y=2, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=9, your_checker=False, x=3, y=2, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=10, your_checker=False, x=5, y=2, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=11, your_checker=False, x=7, y=2, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=12, your_checker=False, x=0, y=5, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=1, y=4)]),
            Checker(checker_num=13, your_checker=False, x=2, y=5, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=1, y=4), PossibleMove(x=3, y=4)]),
            Checker(checker_num=14, your_checker=False, x=4, y=5, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=3, y=4), PossibleMove(x=5, y=4)]),
            Checker(checker_num=15, your_checker=False, x=6, y=5, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=5, y=4), PossibleMove(x=7, y=4)]),
            Checker(checker_num=16, your_checker=False, x=1, y=6, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=17, your_checker=False, x=3, y=6, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=18, your_checker=False, x=5, y=6, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=19, your_checker=False, x=7, y=6, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=20, your_checker=False, x=0, y=7, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=21, your_checker=False, x=2, y=7, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=22, your_checker=False, x=4, y=7, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=23, your_checker=False, x=6, y=7, checker_type=CheckerType.WHITE, possible_moves=[]),
        ]

        self.assertSetEqual(
            set(game_state.checkers),
            set(checkers_true),
        )


if __name__ == "__main__":
    unittest.main()
