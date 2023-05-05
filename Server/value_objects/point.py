"""Module define point of field."""


class Point:
    """Point of field in game."""

    def __init__(self, x: int = -1, y: int = -1):
        """Initialize point of field in game."""
        self.__x = x
        self.__y = y

    @property
    def x(self):
        """Get coordinate by axis x."""
        return self.__x

    @property
    def y(self):
        """Get coordinate by axis y."""
        return self.__y

    def __eq__(self, other):
        """Check equality of two objects."""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y

        return NotImplemented
