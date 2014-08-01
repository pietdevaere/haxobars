from haxosender import *

if __name__ == "__name__":

    camp = Camp("31.22.123.224")
    for i in range(20):
        camp.add_light('bar', 1 + i*19, i*4)

    camp.set_light(14, (0, 255, 0, 0))
    camp.transmit()
