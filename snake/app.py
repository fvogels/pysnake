import pygame
import sys


FRAMES_PER_SECOND = 75
GRID_SIZE = (32, 32)
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


def create_display_surface():
    grid_width, grid_height = GRID_SIZE
    surface_width = grid_width * CELL_SIZE
    surface_height = grid_height * CELL_SIZE
    surface_size = (surface_width, surface_height)
    return pygame.display.set_mode(surface_size)


def create_grid():
    width, height = GRID_SIZE
    grid = [
        [Empty() for _ in range(width)]
        for _ in range(height)
    ]
    for x in range(width):
        grid[0][x] = grid[height-1][x] = Wall()
    for y in range(height):
        grid[y][0] = grid[y][width-1] = Wall()
    return grid


def render_grid(surface, grid):
    width, height = GRID_SIZE
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            color = cell.color
            rectangle = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rectangle)


# Initialize Pygame
pygame.init()

# Create window with given size
display_surface = create_display_surface()
clock = pygame.time.Clock()
grid = create_grid()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    display_surface.fill((0,0,0))
    render_grid(display_surface, grid)

    pygame.display.update()
    clock.tick(FRAMES_PER_SECOND)
