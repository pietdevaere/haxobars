from haxosender import *

if __name__ == "__main__":

    camp = Camp('31.22.123.224')
    for i in range(20):
        newLight = camp.add_light('bar', 1 + i*19, i*4)

    k=0
    while True:
        for k in range(2):
            for j in range(20):
                for light in camp.lights:
                    if light.kind != 'bar':
                        continue
                    light.rgba((0, 0, 255, 0))
                for i in range(80):
                    if i % 20 == j:
                        camp.set_light(i, (127, 0, 255, 0))
                        camp.set_light((i+1)%80, (255,0,0,0))
                        camp.set_light((i+2)%80, (255,0,0,0))
                        camp.set_light((i+3)%80, (127,0,255,0))
                camp.transmit()
                sleep(0.005)
  ##      while True:
        for k in range(3):
            for j in range(80):
                camp.set_light(j, (255, 255, 255, 255))
            camp.transmit()
            sleep(0.025)
            for j in range(80):
                camp.set_light(j, (0, 0, 0, 0))
            camp.transmit()
            sleep(0.025)
