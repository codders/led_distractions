#!/usr/bin/env python
'''Space-filling curves and rainbows'''
from __future__ import division
import argparse
import time
import logging
import scurve
import arduino_lights as al
from arduino_lights import LED_SIZE, LED_COUNT
import colorgen


def frange(start, end, step=1.0, steps=0):
    if steps:
        step = (end - start)/steps
    curr = start
    while curr < end:
        yield curr
        curr += step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--curve', help='curve type (default: hilbert)',
                        default='hilbert',
                        choices=['hilbert', 'hcurve', 'zorder', 'zigzag', 'natural', 'gray'])
    parser.add_argument('--rainbow', action='store_true', help='use hilbert rainbow')
    parser.add_argument('--palette-size', type=int, default=3)
    parser.add_argument('--steps', type=int, default=100, help='timesteps to complete a cycle')
    parser.add_argument('--pan', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    curve = scurve.fromSize(args.curve, 2, 256)
    size = len(curve)

    # because the hcurve cannot tell us an index from coordinates,
    # create a map of coordinates to alpha values by iterating over the
    # indices of the curve
    alpha_map = {}
    for i, p in enumerate(curve):
        alpha_map[tuple(p)] = i / size

    colorfn = None
    if args.rainbow:
        colorgen.hilbert_rainbow(args.palette_size)
        colorfn = colorgen.cyclic_gradient
    else:
        colorgen.randomize_palette(args.palette_size, 'triadic')
        colorfn = colorgen.symetric_gradient
    logging.debug('Chose palette %s', str(colorgen.palette))

    pan_speed = 4
    con = al.connect()
    while True:
        for offset in frange(0.0, 15.0, 1.0/args.steps):
            for x in range(LED_SIZE.w):
                for y in range(LED_SIZE.h):
                    # correct for the fact that the 256-point curve (16x16)
                    # does not fit on a 12x12 square
                    p = None
                    if args.pan:
                        p = (int(x + pan_speed*offset) % 16, int(y + pan_speed*offset) % 16)
                    else:
                        p = (x + 2, y + 2)
                    color = colorfn((alpha_map[p] + offset) % 1.0)
                    al.set_pixel(con, (x, y), *color)
            al.end_frame(con)
            time.sleep(0.05)
