import pygame
import random
import sys
from snake.position import Position
from snake.direction import *
from snake.cell import *
from snake.screens import IntroScreen
from snake.timer import Timer
from snake.keybindings import KeyBindings, ActionBuffer
from snake.level import create_level
from snake.screens import *


FRAMES_PER_SECOND = 75

def create_display_surface(surface_size):
    return pygame.display.set_mode(surface_size)


def switch_screen(screen):
    global current_screen
    current_screen = screen


# Initialize Pygame
pygame.init()

display_surface = create_display_surface((1000, 1000))
clock = pygame.time.Clock()
current_screen = IntroScreen(switch_screen)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            current_screen.process_key(event.key)

    current_screen.render(display_surface)
    pygame.display.flip()

    elapsed_seconds = clock.tick(FRAMES_PER_SECOND) / 1000
    current_screen.tick(elapsed_seconds)

