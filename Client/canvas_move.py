"""This module describes checkers moves by canvas."""
from .contracts.value_objects.checker_type import CheckerType


class CanvasMove:
    """Checker move by canvas."""

    def __init__(
        self,
        x,
        y,
        new_type: CheckerType = None,
        remove_checker_num=None,
        remove_checker_icon=None,
    ):
        """Initialize checker move by canvas."""
        self.x: int = x
        self.y: int = y
        self.new_type: CheckerType = new_type
        self.remove_checker_num: int = remove_checker_num
        self.remove_checker_icon: int = remove_checker_icon
