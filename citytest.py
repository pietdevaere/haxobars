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

    universe = [0 for k in range(10)]
    for counter in range(1024):
        binairy = '{0:010b}'.format(counter)
        for i in range(10):
            if binairy[i] == '1':
                universe[i] = 134
            else:
                universe[i] = 0
        print universe
        bars.send([universe])
        sleep(0.1)
        
                

                
