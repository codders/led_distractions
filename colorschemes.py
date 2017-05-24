#!/usr/bin/env python
'''A visualisation of random color schemes, useful to test out the
colorgen module'''
from __future__ import division
import time
import random
import arduino_lights as al
from arduino_lights import LED_SIZE
import colorgen


if __name__ == '__main__':
    random.seed()
    funcs = [
        colorgen.sample_gradient_palette,
        colorgen.sample_palette,
        colorgen.symetric_gradient,
        colorgen.cyclic_gradient
    ]
    bl = al.connect()
    while True:
        colorfn = random.choice(funcs)
        if random.random() < 0.5:
            size = random.randrange(2, 6)
            harmony = random.choice(colorgen.HARMONIES.keys())
            colorgen.randomize_palette(size, harmony)
            print "randomize_palette: size %d, harmony %s, %s" \
                % (size, harmony, colorfn.func_name)
        else:
            size = random.choice([8, 64])
            colorgen.hilbert_rainbow(size)
            print "hilbert_rainbow: size %d, %s" \
                % (size, colorfn.func_name)
        for i in xrange(al.LED_SIZE.w):
            for j in xrange(al.LED_SIZE.h):
                color = colorfn((i + j) / (LED_SIZE.w + LED_SIZE.h - 2))
                al.set_pixel(bl, (i, j), *color)
        al.end_frame(bl)
        time.sleep(5)
