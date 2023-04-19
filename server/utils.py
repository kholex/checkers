# TODO: remove mock
class Checker:
    pass

# TODO: remove mock
class CheckerType:
    pass


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
                1/0  # TODO: raise error
        

            checker = Checker(
                checker_num=i,
                your_checker=None,  # TODO
                x=x,
                y=y,
                checker_type=checker_type,
                possible_moves=None,  # TODO
            )
            checker_list.append(checker)
            i += 1
    return checker_list
