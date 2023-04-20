class Direction:
    def __init__(self, dx, dy):
        self.__dx = dx
        self.__dy = dy

    @property
    def dx(self):
        return self.__dx

    @property
    def dy(self):
        return self.__dy

    def __repr__(self):
        return f'Direction({self.dx}, {self.dy})'

    def __str__(self):
        return f'({self.dx}, {self.dy})'


EAST = Direction(1, 0)
WEST = Direction(-1, 0)
NORTH = Direction(0, -1)
SOUTH = Direction(0, 1)
