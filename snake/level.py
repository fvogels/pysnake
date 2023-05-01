from snake.grid import Grid
from snake.position import Position
import snake.direction as direction
from snake.cell import *


class Level:
    def __init__(self, width, height):
        self.__grid = self.__create_empty_grid(width, height)

    def __create_empty_grid(self, width, height):
        def initialize(position):
            x = position.x
            y = position.y
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                return WALL
            else:
                return EMPTY

        return Grid(width, height, initialize)

    @property
    def width(self):
        return self.__grid.width

    @property
    def height(self):
        return self.__grid.height

    def __getitem__(self, position):
        return self.__grid[position]

    def __setitem__(self, position, value):
        self.__grid[position] = value


def create_level():
    level = Level(32, 32)
    tail = Position(15, 16)
    head = Position(16, 16)

    level[tail] = SnakeSegment(next=head)
    level[head] = SnakeHead()

    return (level, head, tail, direction.EAST)
