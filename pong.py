import serial, Image
import time, math
from arduino_lights import ledutils

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200
)

# So! Apparently when you connect to the arduino serial port, the bootloader
# kicks in, resets the arduino and waits a second for a new program to be loaded
# before running the actual already stored code 
time.sleep(2)

def paddel(x, y):
  for h in range(y-1, y+2):
    ledutils.set_pixel(ser, x, h, 0, 255, 0)

def clear():
  for x in range(0, 12):
    for y in range(0, 12):
      ledutils.set_pixel(ser, x, y, 0, 0, 0)

ballx = 5
bally = 11
deltax = -1
deltay = 1
paddels = [5, 7]
while(True):
  clear()

  if ballx == 10 or ballx == 1:
    deltax = -deltax
  if bally == 11 or bally == 0:
    deltay = -deltay
  ballx = ballx + deltax
  bally = bally + deltay

  active_paddel = 0
  if deltax > 0:
    active_paddel = 1

  ledutils.set_pixel(ser, ballx, bally, 0, 255, 0) 

  if paddels[active_paddel] != bally:
    diff = bally - paddels[active_paddel]
    paddels[active_paddel] = paddels[active_paddel] + (diff / abs(diff))
    if paddels[active_paddel] == 0:
      paddels[active_paddel] = 1
    if paddels[active_paddel] == 11:
      paddels[active_paddel] = 10
  paddel(0, paddels[0])
  paddel(11, paddels[1])
 
  ledutils.end_frame(ser)
  time.sleep(0.05)
