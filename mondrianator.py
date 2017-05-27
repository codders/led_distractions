#!/usr/bin/env python
'''Composition in Red, Blue and Yellow art generator'''
import time
import argparse
from random import choice, randint, random
import math
from itertools import product
import arduino_lights as al
from arduino_lights import LED_SIZE, LED_COUNT


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

painting = {xy: WHITE
            for xy in product(xrange(LED_SIZE.w), xrange(LED_SIZE.h))}

lines = set()
paints = 0
active_lines = []
active_paints = []


def add_line():
    while True:
        line = (choice(['h', 'v']),
                choice(xrange(LED_SIZE.w)))
        if line not in lines \
            and (line[0], line[1]+1) not in lines \
            and (line[0], line[1]-1) not in lines:
            break
    lines.add(line)
    direction = choice([-1, 1])
    current = -1 if direction == 1 else LED_SIZE.h
    active_lines.append({
        'orientation': line[0],
        'position': line[1],
        'direction': direction,
        'current': current,
        'done': False
    })
    print "Added line %s" % str(active_lines[-1])


def add_paint():
    global paints
    while True:
        xy = (randint(0, LED_SIZE.w - 1), randint(0, LED_SIZE.h - 1))
        if painting[xy] == WHITE:
            break
    active_paints.append({
        'origin': xy,
        'color': choice([RED, BLUE, YELLOW]),
        'done': False,
    })
    paints += 1
    print "Added paint %s" % str(active_paints[-1])


def grow_paints():
    global active_paints
    for paint in active_paints:
        if 'perimeter' not in paint:
            paint['perimeter'] = {paint['origin']}
            painting[paint['origin']] = paint['color']
        else:
            new_perimeter = set()
            for point in paint['perimeter']:
                # paint all neighbours of perimeter that are white
                for direction in product([-1, 0, 1], [-1, 0, 1]):
                    if direction[0] == direction[1] == 0:
                        continue
                    neighbour = (point[0] + direction[0], point[1] + direction[1])
                    if any(d < 0 or d >= LED_SIZE.h for d in neighbour):
                        continue
                    if painting[neighbour] == WHITE:
                        painting[neighbour] = paint['color']
                        new_perimeter.add(neighbour)
            if len(new_perimeter) == 0:
                paint['done'] = True
            else:
                paint['perimeter'] = new_perimeter
    active_paints = [p for p in active_paints if not p['done']]


def grow_lines():
    global active_lines
    def orient(x, y, orientation):
        if orientation == 'v':
            return (x, y)
        else:
            return (y, x)

    W, H = LED_SIZE
    for line in active_lines:
        line['current'] += line['direction']
        if  line['current'] < 0 or line['current'] >= W:
            line['done'] = True
            continue
        point = (line['position'], line['current'])

        o = line['orientation']
        adjacent = [((point[0] + i) % W, point[1]) for i in (-1, 1)]
        if any(painting[orient(*a, orientation=o)] == BLACK for a in adjacent):
            # we have just intersected another line, maybe end?
            if random() < 0.25:
                line['done'] = True

        # transform
        point = orient(*point, orientation=o)

        # paint line
        painting[point] = BLACK

    active_lines = [l for l in active_lines if not l['done']]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args()
    blbox = al.connect()
    # random.seed()

    PROB_LINE = 0.5
    PROB_COLOR = 0.30

    while True:
        al.draw_pixel_map(blbox, painting)
        grow_lines()
        grow_paints()

        if random() < PROB_LINE**len(lines):
            add_line()
        if len(lines) > 4 and random() < PROB_COLOR**paints:
            add_paint()

        time.sleep(0.1)
