from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep

# universe = [ 255,255,64, 255,255,64, 255,255,64, 255,255,64 ]
universe = [ 255,172,0, 255,172,0, 255,172,0, 255,172,0 ]

def sendValues(array):
        ip=IP(dst='31.22.122.55',src='31.22.122.24')
        udp=UDP(sport=6454,dport=6454)

        artnet=ArtNet()
        artdmx=ArtDMX()

        artdmx.setfieldval("universe", 0)
        artdmx.setfieldval("subnet", 0)

        flatValues=list(itertools.chain.from_iterable(array));

        #print flatValues

        artdmx.setfieldval("length", len(flatValues))

        dmxarray=[]
        for i in range(len(flatValues)):
            dmxarray.append(chr(int(hex(flatValues[i]),16)))

        #print dmxarray

        payload=''.join(dmxarray)

        paquete=ip/udp/artnet/artdmx/payload

        #paquete.display()

        send(paquete)

if __name__ == "__main__":
    while True:
        for y in range(0,100):
            for j in range(0,19):
                array=[]
                for i in range(0,19):
                    if i%10 == j%10:
                        array.append([0,0,255,0,255,0])
                    else:
                        array.append([255,0,0,0,255,0])
                sendValues(array)
                sleep(0.1)
        for x in range(0,2):
            array=[]
            for j in range(0,19):
                array.append([0,0,255,0,255,0])
            sendValues(array)
            sleep(0.1)

            for j in range(0,19):
                array.append([255,0,0,0,255,0])
            sendValues(array)
            sleep(0.4)
                

                
