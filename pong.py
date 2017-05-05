import serial, Image
import time, math
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200
)

# So! Apparently when you connect to the arduino serial port, the bootloader
# kicks in, resets the arduino and waits a second for a new program to be loaded
# before running the actual already stored code 
time.sleep(2)

def set_pixel(pixel, red, green, blue):
  red   = min(red, 253)
  green = min(green, 253)
  blue  = min(blue, 253)

  control_string = bytearray([pixel,red,green,blue, 255])
  ser.write(control_string)    

def xy_to_pixel(x,y):
  row_offset = y * 12
  if y % 2 == 0:
    column_offset = (11 - x)
  else:
    column_offset = x
  return row_offset + column_offset

def render_image(image_path):
  img = Image.open("images/" + image_path)
  rgb_im = img.convert('RGB')
  size = 12,12
  #rgb_im.thumbnail(size, Image.ANTIALIAS)
  sleep_time = 0.002
  #sleep_time = 0.01

  control_string = bytearray([254])
  ser.write(control_string)  


  print "time per frame: " + str(sleep_time * 144) + "s"

  for x in range(12):
    for y in range(12):
      r,g,b = rgb_im.getpixel((x,y))
      pixel = xy_to_pixel(x,11 - y)
      set_pixel(pixel,r,g,b)
      #time.sleep(sleep_time)

def paddel(x, y):
  for h in range(y-1, y+2):
    set_pixel(xy_to_pixel(x, h), 0, 255, 0)

def clear():
  for x in range(0, 12):
    for y in range(0, 12):
      set_pixel(xy_to_pixel(x, y), 0, 0, 0)

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

#  print "x:", ballx, "y:", bally, "pl:", paddels[0], "pr:", paddels[1], "ac:", active_paddel
  set_pixel(xy_to_pixel(ballx, bally), 0, 255, 0) 

  if paddels[active_paddel] != bally:
    diff = bally - paddels[active_paddel]
    paddels[active_paddel] = paddels[active_paddel] + (diff / abs(diff))
    if paddels[active_paddel] == 0:
      paddels[active_paddel] = 1
    if paddels[active_paddel] == 11:
      paddels[active_paddel] = 10
  paddel(0, paddels[0])
  paddel(11, paddels[1])
 
  ser.write(bytearray([254]))
  time.sleep(0.05)
