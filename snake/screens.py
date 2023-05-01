from abc import ABC, abstractmethod
from snake.keybindings import ActionBuffer, KeyBindings
import pygame
import snake.actions as actions
from snake.state import State
from snake.level import create_level
from snake.position import Position


class Screen(ABC):
    def __init__(self, switch_screen):
        self._switch_screen = switch_screen

    @abstractmethod
    def render(self, display_surface):
        ...

    @abstractmethod
    def tick(self, elapsed_seconds):
        ...

    @abstractmethod
    def process_key(self, key):
        ...


class IntroScreen(Screen):
    def __init__(self, switch_screen):
        super().__init__(switch_screen)
        font = pygame.font.SysFont(None, 128)
        self.__buffer = font.render('Snake!', True, pygame.Color('red'))
        self.__width, self.__height = self.__buffer.get_size()

    def render(self, display_surface):
        display_surface.fill(pygame.Color('black'))
        width, height = display_surface.get_size()
        x = (width - self.__width) / 2
        y = (height - self.__height) / 2
        display_surface.blit(self.__buffer, (x, y))

    def tick(self, elapsed_seconds):
        pass

    def process_key(self, key):
        if key == pygame.K_SPACE:
            self._switch_screen(GameScreen(self._switch_screen))


class GameScreen(Screen):
    def __init__(self, switch_screen):
        super().__init__(switch_screen)
        self.__key_bindings = KeyBindings()
        self.__action_buffer = ActionBuffer()
        self.__key_bindings.bind(pygame.K_LEFT, self.__action_buffer, actions.LEFT)
        self.__key_bindings.bind(pygame.K_RIGHT, self.__action_buffer, actions.RIGHT)
        self.__key_bindings.bind(pygame.K_UP, self.__action_buffer, actions.UP)
        self.__key_bindings.bind(pygame.K_DOWN, self.__action_buffer, actions.DOWN)
        self.__state = State(create_level, self.__action_buffer)

    def process_key(self, key):
        self.__key_bindings.process_key(key)

    def render(self, display_surface):
        level = self.__state.level
        width, height = display_surface.get_size()
        cell_width = width // level.width
        cell_height = height // level.height
        for y in range(level.height):
            for x in range(level.width):
                cell = level[Position(x, y)]
                color = cell.color
                rectangle = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                pygame.draw.rect(display_surface, color, rectangle)

    def tick(self, elapsed_seconds):
        self.__state.tick(elapsed_seconds)
