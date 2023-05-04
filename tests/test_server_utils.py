import unittest
from copy import deepcopy

from Server.game import generate_new_game, Checker, CheckerType, PossibleMove


class TestServerUtils(unittest.TestCase):

    def test_generate_new_game(self):

        white_checkers_list, black_checkers_list = generate_new_game()

        checker_list_true = [
            Checker(checker_num=0, your_checker=None, x=0, y=0, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=1, your_checker=None, x=0, y=2, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=1, y=3)]),
            Checker(checker_num=2, your_checker=None, x=0, y=6, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=3, your_checker=None, x=1, y=1, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=4, your_checker=None, x=1, y=5, checker_type=CheckerType.BLACK, possible_moves=[PossibleMove(x=0, y=4), PossibleMove(x=2, y=4)]),
            Checker(checker_num=5, your_checker=None, x=1, y=7, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=6, your_checker=None, x=2, y=0, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=7, your_checker=None, x=2, y=2, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=1, y=3), PossibleMove(x=3, y=3)]),
            Checker(checker_num=8, your_checker=None, x=2, y=6, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=9, your_checker=None, x=3, y=1, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=10, your_checker=None, x=3, y=5, checker_type=CheckerType.BLACK, possible_moves=[PossibleMove(x=2, y=4), PossibleMove(x=4, y=4)]),
            Checker(checker_num=11, your_checker=None, x=3, y=7, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=12, your_checker=None, x=4, y=0, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=13, your_checker=None, x=4, y=2, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=3, y=3), PossibleMove(x=5, y=3)]),
            Checker(checker_num=14, your_checker=None, x=4, y=6, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=15, your_checker=None, x=5, y=1, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=16, your_checker=None, x=5, y=5, checker_type=CheckerType.BLACK, possible_moves=[PossibleMove(x=4, y=4), PossibleMove(x=6, y=4)]),
            Checker(checker_num=17, your_checker=None, x=5, y=7, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=18, your_checker=None, x=6, y=0, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=19, your_checker=None, x=6, y=2, checker_type=CheckerType.WHITE, possible_moves=[PossibleMove(x=5, y=3), PossibleMove(x=7, y=3)]),
            Checker(checker_num=20, your_checker=None, x=6, y=6, checker_type=CheckerType.BLACK, possible_moves=[]),
            Checker(checker_num=21, your_checker=None, x=7, y=1, checker_type=CheckerType.WHITE, possible_moves=[]),
            Checker(checker_num=22, your_checker=None, x=7, y=5, checker_type=CheckerType.BLACK, possible_moves=[PossibleMove(x=6, y=4)]),
            Checker(checker_num=23, your_checker=None, x=7, y=7, checker_type=CheckerType.BLACK, possible_moves=[]),
        ]

        white_checkers_list_true = deepcopy(checker_list_true)
        for checker in white_checkers_list_true:
            if checker.checker_type == CheckerType.WHITE:
                checker.your_checker = True
            elif checker.checker_type == CheckerType.BLACK:
                checker.your_checker = False

        black_checkers_list_true = deepcopy(checker_list_true)
        for checker in black_checkers_list_true:
            if checker.checker_type == CheckerType.WHITE:
                checker.your_checker = False
            elif checker.checker_type == CheckerType.BLACK:
                checker.your_checker = True

        self.assertListEqual(white_checkers_list, white_checkers_list_true)
        self.assertListEqual(black_checkers_list, black_checkers_list_true)


if __name__ == "__main__":
    unittest.main()
