import pygame
import random
import sys
from snake.position import Position
from snake.direction import *
from snake.timer import Timer


FRAMES_PER_SECOND = 75
CELL_SIZE = 32

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)


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


class Food:
    @property
    def color(self):
        return GREEN


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

    return (level, head, tail, EAST)



class Input:
    def __init__(self):
        self.__inputs = None

    def reset(self):
        self.__inputs = None

    def __update(self):
        if not self.__inputs:
            self.__inputs = pygame.key.get_pressed()

    def __is_pressed(self, key):
        self.__update()
        return self.__inputs[key]

    @property
    def up(self):
        return self.__is_pressed(pygame.K_UP)

    @property
    def down(self):
        return self.__is_pressed(pygame.K_DOWN)

    @property
    def left(self):
        return self.__is_pressed(pygame.K_LEFT)

    @property
    def right(self):
        return self.__is_pressed(pygame.K_RIGHT)

    @property
    def direction(self):
        if self.up:
            return NORTH
        if self.down:
            return SOUTH
        if self.left:
            return WEST
        if self.right:
            return EAST
        return None


class State:
    def __init__(self, level_factory):
        self.__level, self.__snake_head, self.__snake_tail, self.__move_direction = level_factory()
        self.__input = Input()
        self.__move_timer = Timer(0.1)
        self.__food_timer = Timer(1)
        self.__snake_growth = 0

    @property
    def level(self):
        return self.__level

    def advance_head(self, direction):
        old_snake_head = self.__snake_head
        new_snake_head = old_snake_head + direction
        self.__level[old_snake_head].next = new_snake_head
        self.__level[new_snake_head] = SnakeSegment()
        self.__snake_head = new_snake_head

    def advance_tail(self):
        old_snake_tail = self.__snake_tail
        new_snake_tail = self.__level[old_snake_tail].next
        self.__level[old_snake_tail] = Empty()
        self.__snake_tail = new_snake_tail

    def tick(self, elapsed_seconds):
        self.__input.reset()
        self.__update_food(elapsed_seconds)
        self.__update_movement(elapsed_seconds)

    def __find_random_empty_cell(self):
        while True:
            x = random.randint(0, self.__level.width - 1)
            y = random.randint(0, self.__level.height - 1)
            position = Position(x, y)
            if isinstance(self.__level[position], Empty):
                return position


    def __update_food(self, elapsed_seconds):
        self.__food_timer.tick(elapsed_seconds)
        if self.__food_timer.ready:
            self.__food_timer.consume()
            position = self.__find_random_empty_cell()
            self.__level[position] = Food()

    def __update_movement(self, elapsed_seconds):
        self.__move_direction = self.__input.direction or self.__move_direction
        self.__move_timer.tick(elapsed_seconds)
        if self.__move_timer.ready:
            self.__move_timer.consume()
            self.advance_head(self.__move_direction)
            if self.__snake_growth == 0:
                self.advance_tail()
            else:
                self.__snake_growth -= 1


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
    pygame.display.flip()

    elapsed_seconds = clock.tick(FRAMES_PER_SECOND) / 1000
    state.tick(elapsed_seconds)
