from copy import deepcopy
from typing import List, Tuple

from Client.contracts.value_objects.checker import Checker
from Client.contracts.value_objects.checker_type import CheckerType
from Client.contracts.value_objects.possible_move import PossibleMove


def generate_new_game() -> Tuple[List[Checker], List[Checker]]:
    """TODO"""

    i = 0
    white_checkers_list: List[Checker] = []
    
    for x in range(8):
        if x % 2 == 0:
            y_list = [0, 2, 6]
        else:
            y_list = [1, 5, 7]
        for y in y_list:

            # checker_type
            if y < 3:
                checker_type = CheckerType.WHITE
                your_checker = True
            elif y > 4:
                checker_type = CheckerType.BLACK
                your_checker = False
            else:
                raise RuntimeError("Checkers initialization error, impossible position.")
        
            checker = Checker(
                checker_num=i,
                your_checker=your_checker,
                x=x,
                y=y,
                checker_type=checker_type,
                possible_moves=[],
            )
            white_checkers_list.append(checker)
            i += 1
    
    black_checkers_list = deepcopy(white_checkers_list)
    for checker in black_checkers_list:
        checker.your_checker = not checker.your_checker

    return white_checkers_list, black_checkers_list


def get_possible_moves(checker: Checker) -> List[PossibleMove]:
    """TODO"""

    x, y = checker.x, checker.y
    possible_moves = []

    if y == 2:  # white
        if x != 0:
            possible_moves.append(PossibleMove(x=x-1, y=3))
        if x != 7:
            possible_moves.append(PossibleMove(x=x+1, y=3))
    elif y == 5:  # black
        if x != 0:
            possible_moves.append(PossibleMove(x=x-1, y=4))
        if x != 7:
            possible_moves.append(PossibleMove(x=x+1, y=4))
    
    return possible_moves
