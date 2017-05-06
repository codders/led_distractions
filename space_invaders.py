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
