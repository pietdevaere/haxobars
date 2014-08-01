from haxosender import *
from time import sleep

black = (0, 0, 0, 0)
white = (255, 255, 255, 255)
blue = (0, 0, 255, 0)
green = (0, 255, 0, 0)

if __name__ == "__main__":

    while True:
        camp = Camp("31.22.123.224")

        for i in range(20):
            camp.add_light('bar', 1 + i*19, i*4)
        
        camp.add_light('eurospot', 381, 80)

        for i in range(80):
            camp.set_light(i, green)

        camp.set_light(80, (0, 255, 0))
        camp.transmit()
        sleep(5)
