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


def symetric_gradient(alpha):
    assert alpha <= 1.0
    if alpha < 0.5:
        return colorgen.sample_gradient_palette(2*alpha)
    else:
        return colorgen.sample_gradient_palette(2*(1 - alpha))


def frange(start, end, step=1.0, steps=0):
    if steps:
        step = (start - end)/steps
    curr = start
    while curr < end:
        yield curr
        curr += step


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--curve', help='curve type (default: hilbert)',
                        default='hilbert',
                        choices=['hilbert', 'zorder', 'zigzag', 'natural'])
    parser.add_argument('--palette-size', type=int, default=3)
    parser.add_argument('--steps', type=int, default=30)
    parser.add_argument('--pan', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    # h = scruve.hilbert.Hilbert(2, 4)
    h = scurve.fromSize(args.curve, 2, 256)
    size = len(h)
    colorgen.randomize_palette(args.palette_size, 'triadic')
    logging.debug('Chose palette %s', str(colorgen.palette))

    con = al.connect()
    while True:
        for offset in frange(0.0, 1.0, steps=args.steps):
            for x in range(LED_SIZE.w):
                for y in range(LED_SIZE.h):
                    # correct for the fact that the 256-point curve (16x16)
                    # does not fit on a 12x12 square
                    if args.pan:
                        p = [int(x + 4*offset), int(y + 4*offset)]
                    else:
                        p = [x + 2, y + 2]
                    a = h.index(p) / size
                    color = symetric_gradient((a + offset) % 1.0)
                    al.set_pixel(con, (x, y), *color)
            al.end_frame(con)
            time.sleep(0.05)
