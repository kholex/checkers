from CheckerType import CheckerType


class PossibleMove:
    def __init__(self, x: int, y: int, new_type: CheckerType = None, remove_checker_num: int = None):
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num
