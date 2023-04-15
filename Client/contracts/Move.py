from CheckerType import CheckerType


class Move:
    def __init__(self, checker_num: int, x: int, y: int, new_type: CheckerType = None, remove_checker_num: int = None):
        self.checker_num: int = checker_num
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num
