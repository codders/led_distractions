'''A module to centralize color palette and scheme generation for the
different visualisations.
'''
from __future__ import division
import colorsys
import random
import operator
from itertools import izip


# Global palette, yes, we're hacking here!
palette = [
    (20, 10, 64),
    (128, 128, 255),
    # (255, 16, 100)
]


def sample_palette(alpha):
    '''Map a float in range [0, 1] into the palette'''
    return palette[int(alpha * len(palette))]


def sample_gradient_palette(alpha):
    '''Maps floats in the range [0, 1] into a smooth, linear gradient
    generated from the palette'''
    idx = int((len(palette) - 1) * alpha)
    color1 = palette[idx]
    if alpha == 1.0:
        return color1  # no next color
    color2 = palette[idx + 1]
    # linearly interpolate between these two
    return tuple(int(color1[c] + (color2[c] - color1[c]) * alpha)
                 for c in range(3))


# Settings for the following function to get different color harmonies
HARMONIES = {
    'complementary': (180, 0, 45, 45, 0),
    'split-complementary': (150, 210, 30, 30, 30),
    'triadic': (120, 240, 30, 30, 30),
    'analogous': (30, 60, 15, 15, 15)
}


def random_hue_harmony(count, offset1, offset2, range0, range1, range2):
    '''This randomly selects hues from around the color wheel, while
    constraining the angle to be within one of three ranges such that:
        - the center of range1 is offset1 degrees from the center of range0
        - the center of range2 if offset2 degrees from the center of range0
    For example, for a complementary color scheme, we want two narrow ranges
    which are on opposite sides of the color wheel, so range0 = range1 = 15,
    range2 = 0 and offset1 = 180 (offset2 can be 0)

    Ported from http://devmag.org.za/2012/07/29/how-to-choose-colours-procedurally-algorithms and modified so that the
    offsets are from the centers of the ranges, to make it more intuitive
    and less annoyance to figure out the angles.
    '''
    hues = []
    ref_angle = random.randint(0, 360)
    r, last_r = -1, -1
    while len(hues) < count:
        angle = random.random() * (range0 + range1 + range2)
        if angle < range0:
            angle -= range0 / 2
            r = 0
        elif angle < range0 + range1:
            angle += offset1 - range1
            r = 1
        else:
            angle += offset2 - range2
            r = 2
        if r == last_r:
            continue  # avoid picking from the same range twice in a row
        last_r = r
        hues.append(((ref_angle + angle) / 360.0) % 1.0)
    return hues


def hue_harmony(count, offset1, offset2, range0, range1, range2):
    '''Fuck it, let's no randomize the range'''
    pass


def to_int_color(float_color):
    return tuple(int(c * 255) for c in float_color)


def noop(x):
    return x


def linear(a, b):
    return lambda x: a + (b - a) * x


def const(a):
    return lambda x: a


def rand(a=0.0, b=1.0):
    return lambda x: a + (b - a) * random.random()


def randomize_palette(n=2, harmony='triadic',
                      lightfn=linear(0.15, 0.75),
                      satfn=rand(0.5, 1.0)):
    '''Generate a random palette of size n with the given hue harmony
    scheme and lightness and saturation generation functions.
    These last two are functions that map the domain [0,1] to a value for
    the relevant color component.
    '''
    global palette
    if isinstance(harmony, basestring):
        if harmony not in HARMONIES:
            raise ValueError('Color harmony not available')
        harmony = HARMONIES[harmony]
    hues = random_hue_harmony(n, *harmony)

    lightnesses = [lightfn(i / (n - 1)) for i in xrange(n)]
    random.shuffle(lightnesses)

    saturations = [satfn(i / (n - 1)) for i in xrange(n)]
    random.shuffle(saturations)

    palette = list(to_int_color(colorsys.hls_to_rgb(h, l, s))
                   for h, l, s in izip(hues, lightnesses, saturations))


