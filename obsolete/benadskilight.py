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
    bars = Sender('10.0.0.10')

    for i in range(1):
  ##  while True:
  ##      universe = [0, 0, 0, 0]
  ##      bars.send([universe])
  ##      sleep(0.1)

        universe = [0, 0, 0, 0, 0, 0] ## off
        bars.send([universe])

        raw_input('enter for idle')
        universe = [0, 100, 100, 0, 0, 0] ## idle blue
        bars.send([universe])
        
        raw_input('enter for strobe')
        universe = [255, 255, 255, 0, 255, 0] ## strobing white
        bars.send([universe])

        raw_input('enter for idle')
        universe = [0, 100, 100, 0, 0, 0] ## idle blue
        bars.send([universe])

        raw_input('enter thunder')
        universe = [255, 255, 255, 0, 200, 193] ## 7 collor flash
        bars.send([universe])

        raw_input('enter for idle')
        universe = [0, 100, 100, 0, 0, 0] ## idle blue
        bars.send([universe])
        
        raw_input('enter lightning')
        universe = [255, 255, 255, 0, 150, 130] ## auto rgb
        bars.send([universe])
        
        raw_input('enter for idle')
        universe = [0, 100, 100, 0, 0, 0] ## idle blue
        bars.send([universe])
            
        raw_input('enter for fog')
        universe = [0, 0, 255, 0, 50, 96] ## foggy
        bars.send([universe])
        

        raw_input('enter for idle')
        universe = [0, 100, 100, 0, 0, 0] ## idle blue
        bars.send([universe])
        raw_input('enter for leaving')
        universe = [255, 255, 255, 0, 0, 96] ## fading white
        bars.send([universe])

        raw_input('enter to exit')
                

                
