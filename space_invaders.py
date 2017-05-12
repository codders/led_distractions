import time
import arduino_lights as al

ser = al.connect()

x = 0
y = 0
first = True
while(True):
  if not first:
    al.set_pixel(ser, (x, y), 0, 0, 0)
  first = False
  x = (x + 1) % 12
  if x == 0:
    y = (y + 1) % 12
  al.set_pixel(ser, (x, y), 0, 255, 0)
  al.end_frame(ser)
  time.sleep(0.05)
