from contracts.checker_type import CheckerType


class PossibleMove:
    def __init__(self, x: int, y: int, new_type: CheckerType = None, remove_checker_num: int = None):
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num

    @staticmethod
    def possible_move_decoder(obj):
        return PossibleMove(obj['x'], obj['y'],
                            obj['new_type'] if 'new_type' in obj else None,
                            obj['remove_checker_num'] if 'remove_checker_num' in obj else None)

