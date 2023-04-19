import unittest

from server.utils import generate_new_game, Checker, CheckerType


class TestServerUtils(unittest.TestCase):

    def test_generate_new_game(self):
        checker_list = generate_new_game()
        checker_list_true = [
            Checker(checker_num=0, your_checker=None, x=0, y=0, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=1, your_checker=None, x=0, y=2, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=2, your_checker=None, x=0, y=6, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=3, your_checker=None, x=1, y=1, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=4, your_checker=None, x=1, y=5, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=5, your_checker=None, x=1, y=7, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=6, your_checker=None, x=2, y=0, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=7, your_checker=None, x=2, y=2, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=8, your_checker=None, x=2, y=6, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=9, your_checker=None, x=3, y=1, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=10, your_checker=None, x=3, y=5, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=11, your_checker=None, x=3, y=7, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=12, your_checker=None, x=4, y=0, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=13, your_checker=None, x=4, y=2, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=14, your_checker=None, x=4, y=6, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=15, your_checker=None, x=5, y=1, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=16, your_checker=None, x=5, y=5, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=17, your_checker=None, x=5, y=7, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=18, your_checker=None, x=6, y=0, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=19, your_checker=None, x=6, y=2, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=20, your_checker=None, x=6, y=6, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=21, your_checker=None, x=7, y=1, checker_type=CheckerType.WHITE, possible_moves=None),
            Checker(checker_num=22, your_checker=None, x=7, y=5, checker_type=CheckerType.BLACK, possible_moves=None),
            Checker(checker_num=23, your_checker=None, x=7, y=7, checker_type=CheckerType.BLACK, possible_moves=None),
        ]

        self.assertListEqual(checker_list, checker_list_true)


if __name__ == "__main__":
    unittest.main()
