"""This module describes part of contracts with server about checkers types."""
from enum import Enum


class CheckerType(Enum):
    """Possible types of checkers in game."""

    BLACK = 0
    WHITE = 1
    BLACK_SUPER = 2
    WHITE_SUPER = 3
