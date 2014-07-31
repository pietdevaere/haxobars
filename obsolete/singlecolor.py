from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep
from haxosender import Sender

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

    for i in range(1):
  ##  while True:
  ##      universe = [0, 0, 0, 0]
  ##      bars.send([universe])
  ##      sleep(0.1)

        universe = [[50, 255, 50, 255, 255, 0]]*50 ## idle blue
        bars.send(universe)
                

                
