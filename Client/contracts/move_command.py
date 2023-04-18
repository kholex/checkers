import json
from contracts.value_objects.checker_type import CheckerType


class MoveCommand:
    def __init__(self, checker_num: int, x: int, y: int, new_type: CheckerType = None, remove_checker_num: int = None):
        self.type = "move_command"
        self.checker_num: int = checker_num
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num

    @staticmethod
    def from_json(obj):
        checker_num, x, y = obj['checker_num'], obj['x'], obj['y']
        new_type = CheckerType(obj['new_type']) if 'new_type' in obj else None
        remove_checker_num = obj['remove_checker_num'] if 'remove_checker_num' in obj else None

        return MoveCommand(checker_num, x, y, new_type, remove_checker_num)

    def to_json(self):
        return json.dumps(self.__dict__)
