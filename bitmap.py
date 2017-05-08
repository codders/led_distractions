import Image
import time, math
import arduino_lights as al

ser = al.connect()

def render_image(image_path):
  img = Image.open("images/" + image_path)
  rgb_im = img.convert('RGB')

  sleep_time = 0.002

  al.end_frame(ser)

  print "time per frame: " + str(sleep_time * 144) + "s"

  for x in range(12):
    for y in range(12):
      r,g,b = rgb_im.getpixel((x,y))
      al.set_pixel(ser, x, 11 - y, r, g, b)
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
