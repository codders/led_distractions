import time
from arduino_lights import ledutils

ser = ledutils.serial_port()

x = 0
y = 0
first = True
while(True):
  if not first:
    ledutils.set_pixel(ser, x, y, 0, 0, 0)
  first = False
  x = (x + 1) % 12
  if x == 0:
    y = (y + 1) % 12
  ledutils.set_pixel(ser, x, y, 0, 255, 0)
  ledutils.end_frame(ser)
  time.sleep(0.05)
