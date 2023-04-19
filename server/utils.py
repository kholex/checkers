from Client.contracts.value_objects.checker import Checker
from Client.contracts.value_objects.checker_type import CheckerType
from Client.contracts.value_objects.possible_move import PossibleMove


def generate_new_game():

    i = 0
    checker_list = []
    
    for x in range(8):
        if x % 2 == 0:
            y_list = [0, 2, 6]
        else:
            y_list = [1, 5, 7]
        for y in y_list:

            # checker_type
            if y < 3:
                checker_type = CheckerType.WHITE
            elif y > 4:
                checker_type = CheckerType.BLACK
            else:
                raise RuntimeError("Checkers initialization error, impossible position.")

            # possible moves
            possible_moves = []
            if y == 2:  # white
                if x != 0:
                    possible_moves.append(PossibleMove(x=x-1, y=3))
                if x != 7:
                    possible_moves.append(PossibleMove(x=x+1, y=3))
            elif y == 5:
                if x != 0:
                    possible_moves.append(PossibleMove(x=x-1, y=4))
                if x != 7:
                    possible_moves.append(PossibleMove(x=x+1, y=4))
        
            checker = Checker(
                checker_num=i,
                your_checker=None,  # TODO
                x=x,
                y=y,
                checker_type=checker_type,
                possible_moves=possible_moves,
            )
            checker_list.append(checker)
            i += 1

    return checker_list
