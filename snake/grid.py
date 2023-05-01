from snake.position import Position


class Grid:
    def __init__(self, width, height, initializer):
        assert width >= 0
        assert height >= 0
        self.__grid = [
            [initializer(Position(x, y)) for x in range(width)]
            for y in range(height)
        ]

    @property
    def width(self):
        return len(self.__grid[0])

    @property
    def height(self):
        return len(self.__grid)

    def is_valid_position(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def __getitem__(self, position):
        assert self.is_valid_position(position)
        return self.__grid[position.y][position.x]

    def __setitem__(self, position, value):
        assert self.is_valid_position(position)
        self.__grid[position.y][position.x] = value
