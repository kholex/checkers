from enum import Enum, auto

class SideType(Enum):
    WHITE = auto()
    BLACK = auto()

    def opposite(side):
        if (side == SideType.WHITE):
            return SideType.BLACK
        elif (side == SideType.BLACK):
            return SideType.WHITE
        else: raise ValueError()
