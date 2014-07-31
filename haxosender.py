from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep

class Sender:
    def __init__(self, dst, port =6454):
        self.dst = dst
        self.src = '1.2.3.4'
        self.port = port

        self.ip = IP(dst=self.dst, src=self.src)
        self.udp = UDP(sport=port, dport=port)

        self.artnet=ArtNet()
        self.artdmx = ArtDMX()

    def send(self, array):
        flatValues=list(itertools.chain.from_iterable(array));
        self.artdmx.setfieldval("length", len(flatValues))
        dmxarray=[]
        for i in range(len(flatValues)):
            dmxarray.append(chr(int(hex(flatValues[i]),16)))

        payload=''.join(dmxarray)
        paquete=self.ip/self.udp/self.artnet/self.artdmx/payload

        send(paquete, verbose=0)



# universe = [ 255,255,64, 255,255,64, 255,255,64, 255,255,64 ]
universe = [ 255,172,0, 255,172,0, 255,172,0, 255,172,0 ]


if __name__ == "__main__":
    bars = Sender('31.22.122.55')

    while True:
        for y in range(0,1):
            for j in range(0,19):
                array=[]
                for i in range(0,19):
                    if i%10 == j%10:
                        array.append([0,0,255,0,255,0])
                    else:
                        array.append([255,0,0,0,255,0])
            ##  sendValues(array)
                bars.send(array)
                sleep(0.1)
        for x in range(0,3):
            array=[]
            for j in range(0,19):
                array.append([0,0,255,0,255,0])
          ##  sendValues(array)
            bars.send(array)
            sleep(0.1)

            array=[]
            for j in range(0,19):
                array.append([255,0,0,0,255,0])
         ##  sendValues(array)
            bars.send(array)
            sleep(0.1)
                

                