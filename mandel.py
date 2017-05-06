import time, math
from arduino_lights import ledutils

ser = ledutils.serial_port()

xMax = 12
yMax = 12

vXMin = -2
vXMax = 2
vYMin = -2
vYMax = 2
max_iterations = 16

def pix_to_cmp(x, y):
  return ((x + .5) / xMax - 0.5) * (vXMax - vXMin) + \
         ((y + .5) / yMax - 0.5) * (vYMax - vYMin) * 1j

def palette(k):
  alpha = (1.0 * k / max_iterations)
  max_col = (255, 255, 255)
  return tuple(int(c *  alpha) for c in max_col)


def set_pixels(pix):
  for i in range(xMax):
    for j in range(yMax):
      c = pix_to_cmp(i, j);
      z = c;
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
  for i in range(xMax):
    for j in range(yMax):
      ledutils.set_pixel(ser, i, j, *pix[i, j])
  ledutils.end_frame(ser)


def zoom_viewport(factor, x, y):
  global vXMax, vXMin, vYMax, vYMin
  sizeX = (vXMax - vXMin) / factor
  sizeY = (vYMax - vYMin) / factor
  vXMax = x + sizeX/2
  vXMin = x - sizeX/2
  vYMax = y + sizeY/2
  vYMin = y - sizeY/2

# pix = list(list((0, 0, 0) for i in range(xMax)) for j in range(xMax))
from PIL import Image
img = Image.new('RGB', (xMax, yMax), 'black')
pix = img.load()

while True:
  set_pixels(pix)
  zoom_viewport(1.5, -1.257, 0.378)
  show_frame(pix)
  time.sleep(1)
  # img.show()
