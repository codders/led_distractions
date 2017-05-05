import serial
import time, math
ser = serial.Serial(
    #port='/dev/ttyACM0',
    port='/dev/ttyUSB0',
    baudrate=57600
)

# So! Apparently when you connect to the arduino serial port, the bootloader
# kicks in, resets the arduino and waits a second for a new program to be loaded
# before running the actual already stored code 
time.sleep(2)

def set_pixel(pixel, red, green, blue):
  red   = min(red, 254)
  green = min(green, 254)
  blue  = min(blue, 254)

  control_string = bytearray([pixel,red,green,blue, 255])
  ser.write(control_string)    

def xy_to_pixel(x,y):
  row_offset = y * 12
  if y % 2 == 0:
    column_offset = (11 - x)
  else:
    column_offset = x
  return row_offset + column_offset

def blink_pixel(x,y):
  pixel = xy_to_pixel(x,y)
  set_pixel(pixel, 255, 125, 0)
  time.sleep(0.05)
  set_pixel(pixel, 0, 0, 0)



# while(True):
#   for i in range(12):
#     blink_pixel(i,5)
#   for i in range(10):
#     blink_pixel(10-i,5)

while(True):
  for i in range(36):
    angle = math.radians(i * 10)
    x = 5 * math.cos(angle) + 6
    y = 5 * math.sin(angle) + 6
    print x
    #print y

    blink_pixel(int(x),int(y))





