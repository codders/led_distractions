#!/usr/bin/env python
'''Mandelbrot set for the Blinkenlights! 8)'''
from __future__ import division
import time
import random
from collections import namedtuple
from itertools import product
import copy
import arduino_lights as al
from arduino_lights import LED_SIZE, Size
import colorgen
import logging
import argparse

Viewport = namedtuple('Viewport', 'bl tr')

view = None
max_iterations = 2600


def pix_to_cmp(x, y):
    size = (view.tr - view.bl)
    inc = size.real / LED_SIZE.w + size.imag / LED_SIZE.h * 1j
    return view.bl + ((x + .5) * inc.real + (y + .5) * inc.imag * 1j)


def set_pixels(pix):
    histogram = list(0 for i in xrange(max_iterations))
    for i in range(LED_SIZE.w):
        for j in range(LED_SIZE.h):
            c = pix_to_cmp(i, j)
            k = escape_time(c)

            if k >= 0:
                histogram[k] += 1
                pix[i, j] = k
                logging.debug("[%d,%d] => (%.25f,%.25f) escaped in %d",
                              i, j, c.real, c.imag, k)
            else:
                pix[i, j] = -1

    total = sum(histogram)
    color = None
    for i in range(LED_SIZE.w):
        for j in range(LED_SIZE.h):
            k = pix[i, j]
            if k >= 0:
                alpha = sum(histogram[0:k]) / total
                color = colorgen.sample_gradient_palette(alpha)
            else:
                color = (0, 0, 0)
            pix[i, j] = color


def escape_time(c):
    '''Return how many iterations it takes the given complex number c to
    diverge enough that we know it's not in the Mandelbrot set.
    Return -1 when it doesn't diverge within max_iterations.'''
    z = c
    for k in range(max_iterations):
        z = z**2 + c
        if z.real**2 + z.imag**2 >= 4.0:
            return k
    else:
        return -1


def zoom_viewport(factor, target):
    global view
    center = view.bl + (view.tr - view.bl) / 2
    # move the center a small step towards the target point
    newcenter = center + (target - center) * (factor - 1.0)
    # calculate the new viewport from the new center by
    # reducing the distance to bl and tr by factor
    view = Viewport(newcenter + (view.bl - center) / factor,
                    newcenter + (view.tr - center) / factor)


def reset_viewport():
    global view
    view = Viewport(-2 - 2j, 2 + 2j)


# mostly taken from http://colinlmiller.com/fractals/gallery.htm
INTERESTING_POINTS = [
    -1.257368028466541028848 + 0.378730831028625370052j,
    -1.77810334274064037110522326038852639499207961414628307584575173232969154440 + 0.00767394242121339392672671947893471774958985018535019684946671264012302378j,
    -1.985540371654130485531439267191269851811165434636382820704394766801377 + 0.000000000000000000000000000001565120217211466101983496092509512479178j,
    -1.25736802846652839265383159384773654166836713857126000896912753375688559878664765114255696457015368246531973104439755978333044015506759938503739206829441575363669402497147343368904702066174408250247081855416385744218741909521990441308969603994513271641284298225323509381146075334937409491188 + 0.37873083102862491151257052392242106932532193327534173605649141946411779667848532042309666819671311329800095959763206221251386819369531602358854394169140220049675504811341950346171196600590463661845947574424944950533273158558278821586333530950155398785389980291835095955110139525825547062070j,
    -0.70334402671161810883 + 0.24717876921242826205j,
]


def main():
    random.seed()
    ser = al.connect()
    pix = {xy: (0, 0, 0)
           for xy in product(xrange(LED_SIZE.w), xrange(LED_SIZE.h))}

    while True:
        colorgen.randomize_palette(3, 'split-complementary',
                                   lightfn=colorgen.linear(0.2, 0.5),
                                   satfn=colorgen.rand())
        p = random.choice(INTERESTING_POINTS)
        prev_pix = copy.copy(pix)
        equal_frames = 0
        reset_viewport()
        while True:
            set_pixels(pix)
            zoom_viewport(1.1, p)
            al.draw_pixel_map(ser, pix)
            time.sleep(0.1)

            equal_frames = equal_frames + 1 if pix == prev_pix else 0
            if equal_frames > 3:
                # we got to a place where pixels don't change anymore
                break
            prev_pix = copy.copy(pix)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--debug', action='store_true', help='debug logging')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    main()
