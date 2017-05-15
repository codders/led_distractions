#!/usr/bin/env python
from __future__ import division
import time
from collections import deque
import arduino_lights as al
import random
from arduino_lights import LED_SIZE, Size
import colorgen
import logging


COLOR_SNAKE = (0, 0, 0)
COLOR_BG = (30, 200, 40)
COLOR_FOOD = (210, 100, 10)
COLOR_DEAD = (230, 20, 20)

DIRECTIONS = {
    'left': (-1, 0),
    'right': (1, 0),
    'up': (0, -1),
    'down': (0, 1),
}


snake = deque((LED_SIZE.w // 2 - i, LED_SIZE.h // 2)
              for i in reversed(xrange(4)))
snake_points = set(snake)
direction = DIRECTIONS['right']
food = None


def add_food(bl):
    global food
    while food is None or food in snake_points:
        food = (random.randint(0, LED_SIZE.w), random.randint(0, LED_SIZE.h))
    al.set_pixel(bl, food, *COLOR_FOOD)


def choose_direction():
    direction = None
    head, neck = snake[-1], snake[-2]
    dir_backwards = tuple(neck[i] - head[i] % LED_SIZE[i] for i in xrange(2))
    logging.debug('snake %s', snake)
    logging.debug('backwards %s', dir_backwards)
    while True:
        direction = random.choice(DIRECTIONS.values())
        if direction != dir_backwards:
            break  # python, WHY U NO DO WHILE??
    logging.debug('chose %s', direction)
    return direction


if __name__ == '__main__':
    random.seed()
    logging.basicConfig(level=logging.DEBUG)

    bl = al.connect()
    al.clear(bl, *COLOR_BG, autoend=False)
    for p in snake:
        al.set_pixel(bl, p, *COLOR_SNAKE)
    al.end_frame(bl)

    eatten = 0
    while True:
        # logging.debug('snake %s', snake)
        # logging.debug('points %s', snake_points)
        # logging.debug('direction %s', direction)
        head = snake[-1]
        head = ((head[0] + direction[0]) % LED_SIZE.w,
                (head[1] + direction[1]) % LED_SIZE.h)
        if head in snake_points:
            # collision! game over
            for p in snake:
                al.set_pixel(bl, p, *COLOR_DEAD)
            al.end_frame(bl)
            break

        # move snake one frame forward
        snake.append(head)
        snake_points.add(head)
        al.set_pixel(bl, head, *COLOR_SNAKE)

        if head == food:
            # ate the food, got bigger
            food = None
            eatten += 1
        else:
            # didn't eat food, move tail forward
            tail = snake.popleft()
            snake_points.remove(tail)
            al.set_pixel(bl, tail, *COLOR_BG)
        al.end_frame(bl)

        if random.random() < 0.1:
            direction = choose_direction()
        if random.random() < 0.05:
            add_food(bl)

        time.sleep(0.1)
