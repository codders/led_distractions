import serial, Image
import time, math
ser = serial.Serial(
    #port='/dev/ttyACM0',
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
      time.sleep(sleep_time)

while(True):
  render_image("one.bmp")
  time.sleep(3)
  render_image("2.bmp")
  time.sleep(3)
  render_image("3.bmp")
  time.sleep(3)
  render_image("4.bmp")
  time.sleep(3)
  render_image("5.bmp")
  time.sleep(3)
  render_image("nuke.bmp")
  time.sleep(3)
  render_image("star.bmp")
  time.sleep(3)
  render_image("flag.bmp")
  time.sleep(3)
  render_image("x.bmp")
  time.sleep(3)
  render_image("heart.bmp")
  time.sleep(3)