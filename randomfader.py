from haxosender import *

if __name__ == "__main__":
    camp = Camp("31.22.123.224")
    for i in range(20):
        camp.add_light('bar', 1 + i*19, i*4)

    for soft in range(80):
        camp.random_dimmer(soft)
    while True:
        camp.transmit()
        done = camp.do_effects()
        sleep(0.1)
        if done != []:
            for effect in done:
                camp.random_dimmer(effect[0])
                print 'restarted', effect[0]
