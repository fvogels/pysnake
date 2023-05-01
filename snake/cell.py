import pygame


class Empty:
    @property
    def color(self):
        return pygame.Color('black')


class Wall:
    @property
    def color(self):
        return pygame.Color('white')


class SnakeSegment:
    def __init__(self, *, next=None):
        self.next = next

    @property
    def color(self):
        return pygame.Color('red')


class SnakeHead:
    @property
    def color(self):
        return pygame.Color('red4')


class Food:
    @property
    def color(self):
        return pygame.Color('green')


class SpeedBoost:
    @property
    def color(self):
        return pygame.Color('blue')


WALL = Wall()
EMPTY = Empty()
FOOD = Food()
SPEED_BOOST = SpeedBoost()
