import pygame
import sys
from snake.position import Position
from snake.direction import Direction


FRAMES_PER_SECOND = 75
CELL_SIZE = 32

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)


class Empty:
    @property
    def color(self):
        return BLACK


class Wall:
    @property
    def color(self):
        return WHITE


class SnakeSegment:
    def __init__(self, *, next=None):
        self.next = next

    @property
    def color(self):
        return RED


class Level:
    def __init__(self, width, height):
        self.__grid = self.__create_empty_grid(width, height)

    def __create_empty_grid(self, width, height):
        def initialize(x, y):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                return Wall()
            else:
                return Empty()

        return [
            [initialize(x, y) for x in range(width)]
            for y in range(height)
        ]


    @property
    def width(self):
        return len(self.__grid[0])

    @property
    def height(self):
        return len(self.__grid)

    def __getitem__(self, position):
        return self.__grid[position.y][position.x]

    def __setitem__(self, position, value):
        self.__grid[position.y][position.x] = value


def create_level():
    level = Level(32, 32)
    tail = Position(15, 16)
    head = Position(16, 16)

    level[tail] = SnakeSegment(next=head)
    level[head] = SnakeSegment()

    return (level, head, tail)


class State:
    def __init__(self, level_factory):
        self.__level, self.__snake_head, self.__snake_tail = level_factory()

    @property
    def level(self):
        return self.__level

    def advance_head(self, direction):
        old_snake_head = self.__snake_head
        new_snake_head = old_snake_head + direction
        self.__level[old_snake_head].next = new_snake_head
        self.__snake_head = new_snake_head

    def advance_tail(self):
        old_snake_tail = self.__snake_tail
        new_snake_tail = self.__level[old_snake_tail].next
        self.__level[old_snake_tail] = Empty()
        self.__snake_tail = new_snake_tail


def create_display_surface(surface_size):
    return pygame.display.set_mode(surface_size)


def render_level(surface, level):
    for y in range(level.height):
        for x in range(level.width):
            cell = level[Position(x, y)]
            color = cell.color
            rectangle = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rectangle)


# Initialize Pygame
pygame.init()

# Create window with given size
state = State(create_level)
display_surface = create_display_surface((state.level.width * CELL_SIZE, state.level.height * CELL_SIZE))
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    display_surface.fill((0,0,0))
    render_level(display_surface, state.level)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
