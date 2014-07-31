from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep
from haxosender import Sender
from random import randrange


universe = [ 255,172,0, 255,172,0, 255,172,0, 255,172,0 ]

"""
    begin met strobe
    donder
    wind
    lightning
    mist
    vertrekken
"""

if __name__ == "__main__":
    bars = Sender('31.22.122.55')

    universe = [[12, 255, 0, 
                125, 125, 125, 125,
                125, 125, 125, 125,
                125, 125, 125, 125,
                125, 125, 125, 125] for bar in range(20)] ## idle blue

    while True:
        
        for i in range(20):
            for j in range(3, 19):
                current = universe[i][j]
                if current == 255:
                    delta = randrange(-1,1)
                elif current == 0:
                    delta = randrange(0, 2)
                else:
                    delta = randrange(-1, 2)
                universe[i][j] = (current + delta) % 255

        bars.send(universe)
        
        sleep(0.1)
                

                
