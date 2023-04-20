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
