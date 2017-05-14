import time
import arduino_lights as al
import colorsys, random, math, copy
from collections import deque

ser = al.connect()

def clear():
    for x in range(0, 12):
        for y in range(0, 12):
            al.set_pixel(ser, (x, y), 0, 0, 0)

clear()
flames = [ [random.random() * 0.2, random.random(), 0.8 + random.random() * 0.2] for x in range(12) ]
screen = deque([[ [0,0,0] for x in range(12)] for y in range(12)])

def fade(row):
  for hsv in row:
    hsv[0] = math.fmod(hsv[0] + (random.random() * 0.05), 0.2)
    hsv[1] = hsv[1] * 0.8

def shift_up(base, array):
  array.append([ [h[0], h[1], h[2]] for h in base ])
  for row in array:
    fade(row) 
  array.popleft()

def fan_flames(flames):
  for hsv in flames:
    hsv[0] = math.fmod(hsv[0] + 0.05, 0.2)
    hsv[1] = min(max(hsv[1] + 0.1 - random.random() * 0.2, 0),1)
    hsv[2] = min(max(hsv[2] * (1.1 - random.random() * 0.1), 0), 1) 

def draw_fire():
  shift_up(flames, screen)
  fan_flames(flames)
  for y, row in enumerate(screen):
    for x, hsv in enumerate(row):
      rgb = [ int(v * 253) for v in colorsys.hls_to_rgb(hsv[0], hsv[1], hsv[2]) ]
      al.set_pixel(ser, (y, x), rgb[0], rgb[1], rgb[2])

while(True):
    draw_fire()

    al.end_frame(ser)
    time.sleep(0.1)
