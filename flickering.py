from haxosender import *

if __name__ == "__main__":
    camp = Camp("31.22.123.224")
    for i in range(20):
        camp.add_light('bar', 1 + i*19, i*4)

    while True:
        for soft in range(80):
            camp.set_light(soft, (255, 0, 0, 0))
        camp.transmit()
        sleep(0.01)
        
        for soft in range(80):
            camp.set_light(soft, (0, 0, 255, 0))
        camp.transmit()
        sleep(0.01)
