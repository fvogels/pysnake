import pygame
import sys


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
    def __init__(self, next):
        self.next = next

    @property
    def color(self):
        return RED



class Position:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y


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


class Level:
    def __init__(self):
        self.__grid = self.__create_grid()
        self.__snake_head = (16, 16)
        self.__snake_tail = (15, 16)
        self.__grid[16][16] = SnakeSegment(None)
        self.__grid[16][15] = SnakeSegment(self.__grid[16][16])

    @property
    def width(self):
        return len(self.__grid[0])

    @property
    def height(self):
        return len(self.__grid)

    def __create_grid(self):
        width, height = (32, 32)
        grid = [
            [Empty() for _ in range(width)]
            for _ in range(height)
        ]
        for x in range(width):
            grid[0][x] = grid[height-1][x] = Wall()
        for y in range(height):
            grid[y][0] = grid[y][width-1] = Wall()
        return grid

    def __getitem__(self, position):
        x, y = position
        return self.__grid[y][x]


def create_display_surface(surface_size):
    return pygame.display.set_mode(surface_size)


def render_grid(surface, grid):
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid[(x, y)]
            color = cell.color
            rectangle = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rectangle)


# Initialize Pygame
pygame.init()

# Create window with given size
grid = Level()
display_surface = create_display_surface((grid.width * CELL_SIZE, grid.height * CELL_SIZE))
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    display_surface.fill((0,0,0))
    render_grid(display_surface, grid)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
