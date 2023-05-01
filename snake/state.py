import pygame
import random
import sys
from snake.position import Position
from snake.direction import *
from snake.cell import *
from snake.timer import Timer
from snake.screens import *
import snake.actions as actions



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
    def __init__(self, level_factory, action_buffer):
        self.__level, self.__snake_head, self.__snake_tail, self.__move_direction = level_factory()
        self.__input = Input()
        self.__move_timer = Timer(0.1)
        self.__bonus_timer = Timer(1)
        self.__snake_growth = 0
        self.__action_buffer = action_buffer

    @property
    def level(self):
        return self.__level

    def __next_head_position(self, direction):
        return self.__snake_head + direction

    def __advance_head_to(self, new_snake_head):
        old_snake_head = self.__snake_head
        self.__level[old_snake_head] = SnakeSegment(next=new_snake_head)
        self.__level[new_snake_head] = SnakeHead()
        self.__snake_head = new_snake_head

    def __advance_tail(self):
        old_snake_tail = self.__snake_tail
        new_snake_tail = self.__level[old_snake_tail].next
        self.__level[old_snake_tail] = EMPTY
        self.__snake_tail = new_snake_tail

    def tick(self, elapsed_seconds):
        self.__input.reset()
        self.__update_bonuses(elapsed_seconds)
        self.__update_movement(elapsed_seconds)

    def __find_random_empty_cell(self):
        while True:
            x = random.randint(0, self.__level.width - 1)
            y = random.randint(0, self.__level.height - 1)
            position = Position(x, y)
            if self.__level[position] is EMPTY:
                return position

    def __update_bonuses(self, elapsed_seconds):
        self.__bonus_timer.tick(elapsed_seconds)
        if self.__bonus_timer.ready:
            self.__bonus_timer.consume()
            position = self.__find_random_empty_cell()
            self.__level[position] = random.choice([FOOD, SPEED_BOOST])

    def __update_movement(self, elapsed_seconds):
        self.__move_timer.tick(elapsed_seconds)
        if self.__move_timer.ready:
            self.__move_timer.consume()
            action = self.__action_buffer.pop()
            if action == actions.LEFT:
                self.__move_direction = WEST
            elif action == actions.RIGHT:
                self.__move_direction = EAST
            elif action == actions.UP:
                self.__move_direction = NORTH
            elif action == actions.DOWN:
                self.__move_direction = SOUTH
            new_snake_head = self.__next_head_position(self.__move_direction)
            destination_contents = self.__level[new_snake_head]
            if destination_contents is FOOD:
                self.__snake_growth += 2
            elif destination_contents is SPEED_BOOST:
                self.__move_timer.delay *= 0.9
            elif destination_contents is not EMPTY:
                sys.exit(0)
            self.__advance_head_to(new_snake_head)
            if self.__snake_growth == 0:
                self.__advance_tail()
            else:
                self.__snake_growth -= 1
