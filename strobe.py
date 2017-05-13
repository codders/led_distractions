import time
import math
import arduino_lights as al

blinken = al.connect()


def blink_pixel(x, y):
    al.set_pixel(blinken, (x, y), 255, 125, 0)
    al.end_frame(blinken)
    time.sleep(0.05)
    al.set_pixel(blinken, (x, y), 0, 0, 0)
    al.end_frame(blinken)


while(True):
    for i in range(36):
        angle = math.radians(i * 10)
        x = 5 * math.cos(angle) + 6
        y = 5 * math.sin(angle) + 6
        print x
        # print y

        blink_pixel(int(x), int(y))
