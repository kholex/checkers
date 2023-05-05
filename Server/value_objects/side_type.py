"""Module define sides in game."""
from enum import Enum, auto


class SideType(Enum):
    """Side in game."""

    WHITE = auto()
    BLACK = auto()

    @staticmethod
    def opposite(side):
        """Get opposite side by current."""
        if side == SideType.WHITE:
            return SideType.BLACK
        elif side == SideType.BLACK:
            return SideType.WHITE
        else:
            raise ValueError()
