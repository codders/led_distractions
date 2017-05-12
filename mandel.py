import time
import math
from collections import namedtuple
from PIL import Image
import arduino_lights as al
from arduino_lights import LED_SIZE

ser = al.connect()

Viewport = namedtuple('Viewport', 'bl tr')

view = Viewport(-2 -2j, 2 + 2j)
max_iterations = 160


def pix_to_cmp(x, y):
  size = (view.tr - view.bl)
  inc = size.real / LED_SIZE.w + size.imag / LED_SIZE.h * 1j
  return view.bl + ((x + .5) * inc.real + (y + .5) * inc.imag * 1j)


def palette(k):
  alpha = (1.0 * k / max_iterations)
  max_col = (255, 255, 255)
  return tuple(int(c * alpha) for c in max_col)


def set_pixels(pix):
  for i in range(LED_SIZE.w):
    for j in range(LED_SIZE.h):
      c = pix_to_cmp(i, j)
      z = c
      for k in range(max_iterations):
        z = z**2 + c

        if z.real**2 + z.imag**2 > 4.0:
          color = palette(k)
          pix[i, j] = color
          print "[%d,%d] => (%.2f,%.2f) escaped in %d => color (%d, %d. %d)" %\
              (i, j, c.real, c.imag, k, color[0], color[1], color[2])
          break
      else:
        pix[i, j] = (0, 0, 0)


def show_frame(pix):
  for i in range(LED_SIZE.w):
    for j in range(LED_SIZE.h):
      al.set_pixel(ser, (i, j), *pix[i, j])
  al.end_frame(ser)


def zoom_viewport(factor, x, y):
  global view
  center = view.bl + (view.tr - view.bl) / 2
  newcenter = x + y * 1j
  view = Viewport(newcenter + (view.bl - center) / factor,
                  newcenter + (view.tr - center) / factor)


img = Image.new('RGB', (LED_SIZE.w, LED_SIZE.h), 'black')
pix = img.load()

while True:
  set_pixels(pix)
  zoom_viewport(1.01, -1.257, 0.378)
  show_frame(pix)
  time.sleep(0.1)
  # img.show()
