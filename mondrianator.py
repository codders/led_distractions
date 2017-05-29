#!/usr/bin/env python
'''Composition in Red, Blue and Yellow art generator'''
import time
import argparse
from random import choice, randint, random, seed
import math
from itertools import product
import arduino_lights as al
from arduino_lights import LED_SIZE, LED_COUNT

PROB_LINE = 0.6
PROB_COLOR = 0.20
PROB_INTERSECT_ENDS = 0.3
MIN_LINES = 3
MAX_LINES = 9
MIN_PAINTS = 3
MAX_PAINTS = 6
DELIGHTMENT_TIME = 10 # seconds

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)


def color_compare(color1, color2):
    '''Produce an ordering of colors so we can settle color-disputes in a field.
    We'll do this in a non-transitive way, so that no color dominates.'''
    # BLACK > COLORS > WHITE
    # COLORS: RED > BLUE, BLUE > YELLOW, YELLOW > RED
    return {
        BLACK: 1,
        RED:    {BLACK: -1, WHITE: 1, RED: 0, BLUE: 1, YELLOW: -1}.get(color2),
        BLUE:   {BLACK: -1, WHITE: 1, RED: -1, BLUE: 0, YELLOW: 1}.get(color2),
        YELLOW: {BLACK: -1, WHITE: 1, RED: 1, BLUE: -1, YELLOW: 0}.get(color2),
        WHITE: -1
    }.get(color1)


def add_line(lines, active_lines):
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
    print "Added line %s" % str(line)


def add_paint(painting, active_paints):
    color = choice([RED, BLUE, YELLOW])
    while True:
        xy = (randint(0, LED_SIZE.w - 1), randint(0, LED_SIZE.h - 1))
        if color_compare(color, painting[xy]) > 0:
            break
    active_paints.append({
        'origin': xy,
        'color': color,
        'done': False,
    })
    print "Added paint %s" % str((xy, color))


def grow_paints(painting, active_paints):
    init = len(active_paints)
    for paint in active_paints:
        if 'perimeter' not in paint:
            paint['perimeter'] = {paint['origin']}
            painting[paint['origin']] = paint['color']
        else:
            new_perimeter = set()
            for point in paint['perimeter']:
                # paint all neighbours of perimeter that are white
                # or less than our color
                for direction in product([-1, 0, 1], [-1, 0, 1]):
                    if direction[0] == direction[1] == 0:
                        continue
                    neighbour = (point[0] + direction[0], point[1] + direction[1])
                    if any(d < 0 or d >= LED_SIZE.h for d in neighbour):
                        continue
                    if color_compare(paint['color'], painting[neighbour]) > 0:
                        painting[neighbour] = paint['color']
                        new_perimeter.add(neighbour)
            if len(new_perimeter) == 0:
                paint['done'] = True
            else:
                paint['perimeter'] = new_perimeter

    active_paints[:] = [p for p in active_paints if not p['done']]  # modify in-place
    return init - len(active_paints)


def grow_lines(painting, active_lines):
    def orient(x, y, orientation):
        if orientation == 'v':
            return (x, y)
        else:
            return (y, x)

    init = len(active_lines)
    for line in active_lines:
        line['current'] += line['direction']
        if  line['current'] < 0 or line['current'] >= LED_SIZE.w:
            line['done'] = True
            continue
        point = (line['position'], line['current'])

        o = line['orientation']
        adjacent = [(point[0] + i, point[1]) for i in (-1, 1)
                    if 0 <= point[0] + i < LED_SIZE.w]
        if any(painting[orient(*a, orientation=o)] == BLACK for a in adjacent):
            # we have just intersected another line, maybe end?
            if random() < PROB_INTERSECT_ENDS:
                line['done'] = True

        point = orient(*point, orientation=o)
        painting[point] = BLACK

    active_lines[:] = [l for l in active_lines if not l['done']]  # modify in-place
    return init - len(active_lines)


def paint_composition(blbox, num_lines, num_paints):
    painting = {xy: WHITE
                for xy in product(xrange(LED_SIZE.w), xrange(LED_SIZE.h))}
    lines = set()
    done_lines = 0
    done_paints = 0
    active_lines = []
    active_paints = []

    while done_lines < num_lines or done_paints < num_paints:
        al.draw_pixel_map(blbox, painting)
        done_lines += grow_lines(painting, active_lines)
        done_paints += grow_paints(painting, active_paints)

        if len(lines) < num_lines and random() < PROB_LINE**len(lines):
            add_line(lines, active_lines)

        paints = done_paints + len(active_paints)
        if (done_lines >= MIN_LINES and paints < num_paints
                and random() < PROB_COLOR**paints):
            add_paint(painting, active_paints)

        time.sleep(0.1)

    print 'Done, now enjoy!'
    time.sleep(DELIGHTMENT_TIME)  # give time to enjoy the resulting pic :)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--min-lines', default=MIN_LINES, type=int)
    parser.add_argument('--max-lines', default=MAX_LINES, type=int)
    parser.add_argument('--min-paints', default=MIN_PAINTS, type=int)
    parser.add_argument('--max-paints', default=MIN_PAINTS, type=int)
    args = parser.parse_args()
    blbox = al.connect()
    seed()

    while True:
        num_lines = randint(args.min_lines, args.max_lines)
        num_paints = randint(args.min_paints, args.max_paints)
        print "Drawing composition with %d lines and %d paints" % (num_lines, num_paints)
        paint_composition(blbox, num_lines, num_paints)
