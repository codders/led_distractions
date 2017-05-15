#!/usr/bin/env python
'''Classic Nokia 6110 snake game'''
from __future__ import division
import time
from collections import deque
import arduino_lights as al
import random
from arduino_lights import LED_SIZE, Size
import colorgen
import logging
import argparse


COLOR_SNAKE = (0, 0, 0)
COLOR_BG = (30, 180, 40)
COLOR_FOOD = (210, 100, 10)
COLOR_DEAD = (230, 20, 20)

DIRECTIONS = {
    # keep things mod(LED_SIZE), makes things nice
    'left': (-1 % LED_SIZE.w, 0),  # (11, 0)
    'right': (1, 0),
    'up': (0, -1 % LED_SIZE.h),  # (0, 11)
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
    logging.debug('food %s', food)
    al.set_pixel(bl, food, *COLOR_FOOD)


def choose_direction():
    new_dir = None
    head, neck = snake[-1], snake[-2]
    backwards = tuple((neck[i] - head[i]) % LED_SIZE[i] for i in xrange(2))
    logging.debug('head %s neck %s: backwards %s', head, neck, backwards)
    while True:
        new_dir = random.choice(DIRECTIONS.values())
        if new_dir != backwards and new_dir != direction:
            break  # python, WHY U NO DO WHILE??
    logging.debug('chose %s', new_dir)
    return new_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--debug', action='store_true', help='debug logging')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    random.seed()

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
        head = tuple((head[i] + direction[i]) % LED_SIZE[i] for i in xrange(2))
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
            logging.debug('ate food! fatness: %d', eatten)
        else:
            # didn't eat food, move tail forward
            tail = snake.popleft()
            snake_points.remove(tail)
            al.set_pixel(bl, tail, *COLOR_BG)
        al.end_frame(bl)

        if random.random() < 0.1:
            direction = choose_direction()
        if food is None and random.random() < 0.15:
            add_food(bl)
        logging.debug('food is at %s', food)

        time.sleep(0.1)
