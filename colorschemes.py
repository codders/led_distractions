#!/usr/bin/env python
'''A visualisation of random color schemes, useful to test out the
colorgen module'''
from __future__ import division
import time
import arduino_lights as al
import colorgen


if __name__ == '__main__':
    bl = al.connect()
    while True:
        for i in xrange(al.LED_SIZE.w):
            for j in xrange(al.LED_SIZE.h):
                color = colorgen.sample_gradient_palette(i / al.LED_SIZE.w)
                al.set_pixel(bl, (i, j), *color)
        al.end_frame(bl)
        colorgen.randomize_palette(harmony='complementary')
        time.sleep(1)
