from contracts.checker_type import CheckerType


class Move:
    def __init__(self, checker_num: int, x: int, y: int, new_type: CheckerType = None, remove_checker_num: int = None):
        self.checker_num: int = checker_num
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num

    @staticmethod
    def move_decoder(obj):
        checker_num, x, y = obj['checker_num'], obj['x'], obj['y']
        new_type = CheckerType(obj['new_type']) if 'new_type' in obj else None
        remove_checker_num = obj['remove_checker_num'] if 'remove_checker_num' in obj else None

        return Move(checker_num, x, y, new_type, remove_checker_num)
