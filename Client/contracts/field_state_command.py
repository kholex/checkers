from contracts.value_objects.checker import Checker


class FieldStateCommand:
    def __init__(self, checkers: list[Checker]):
        self.type = "field_state_command"
        self.checkers = checkers

    @staticmethod
    def field_state_decoder(obj):
        checkers = [Checker.checker_decoder(checker_json) for checker_json in obj["checkers"]]
        return FieldStateCommand(checkers)
