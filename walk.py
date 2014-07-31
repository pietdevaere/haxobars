from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep
from haxosender import Sender

# universe = [ 255,255,64, 255,255,64, 255,255,64, 255,255,64 ]
universe = [ 255,172,0, 255,172,0, 255,172,0, 255,172,0 ]


if __name__ == "__main__":
    bars = Sender('31.22.122.55')

    while True:
        for y in range(0,1):
            for j in range(0,20):
                array=[]
                for i in range(0,20):
                    if i%10 == j%10:
                        array.append([0,0,255,0,255,0])
                    else:
                        array.append([255,0,0,0,255,0])
                bars.send(array)
                sleep(0.1)
        for x in range(0,3):
            array=[]
            for j in range(0,20):
                array.append([0,0,255,0,255,0])
            bars.send(array)
            sleep(0.1)

            array=[]
            for j in range(0,20):
                array.append([255,0,0,0,255,0])
            bars.send(array)
            sleep(0.1)
                

                
