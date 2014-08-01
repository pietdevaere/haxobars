from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep

class Mapper:
    def __init__(self):
        self.table = {}

    def add(self, soft, bar, block = None):
        self.table[soft] = [bar, block]

    def lookup(self, soft):
        return self.table[soft]

class Light:
    def __init__(self, adr, width, kind = None):
        self.adr = adr
        self.width = width
        self.kind = kind
        self.values = [0 for i in range(width)]

    def __repr__(self):
        return(str(self.values))

class City(Light):
    def __init__(self, adr):
        Light.__init__(self, adr, 10, 'city')
        self.values = [255, 0, 0, 0, 255, 0, 0, 0, 0, 0]

    def set_strobe(self, val):
        self.values[7] = val
    

class Bar(Light):
    def __init__(self, adr, width=19):
        Light.__init__(self, adr, width, 'bar')
        self.values = [12, 255, 0,
                       125, 125, 125, 125,
                       125, 125, 125, 125,
                       125, 125, 125, 125, 
                       125, 125, 125, 125]


    def rgba(self, rgbaArray, block = None):
        assert len(rgbaArray) == 4
        if block == None:
            for i in range(4):
                self.rgba(rgbaArray, i)
        else:
            self.values[3 + 4*block: 3 + 4*block + 4] = rgbaArray

class Camp:
    def __init__(self, dst, port = 6454):
        self.lights = set()
        self.resTable = Mapper()
        self.size = 0
        
        self.dst = dst
        self.src = '1.2.3.4'
        self.port = port

        self.ip = IP(dst=self.dst, src=self.src)
        self.udp = UDP(sport=port, dport=port)

        self.artnet=ArtNet()
        self.artdmx = ArtDMX()

    def __repr__(self): ##outdated
        result = ''
        for light in self.lights:
            result += light.kind + ' at adr ' + str(light.adr) + ' with width ' + str(light.width) + '\n'
        return result

    def add_light(self, kind, adr, soft):
        if kind == 'bar':
            newLight = Bar(adr)
            self.lights.add(newLight)
            for i in range(4):
                self.resTable.add(soft + i, newLight, i)
        elif kind == 'city':
            newLight = City(adr)
            self.lights.add(newLight)
            self.resTable.add(soft, newLight)
        return newLight
    
    def set_light(self, soft, val):
        light, block = self.resTable.lookup(soft)
        if light.kind == 'bar':
            light.rgba(val, block)
        elif light.kind == 'city':
            light.set_strobe(val)

    def find_light(self, soft):
        return self.resTable.lookup(soft)

    def get_size(self):
        for light in self.lights:
            if light.adr + light.width > self.size:
                self.size = light.adr + light.width
    


    def transmit(self):
        self.get_size()
        universe = [0 for i in range(self.size)]
        for light in self.lights:
            universe[light.adr - 1: light.adr - 1 + light.width] = light.values
   ##     print universe
        self.artdmx.setfieldval("length", len(universe))
        dmxarray=[]
        for i in range(len(universe)):
            dmxarray.append(chr(int(hex(universe[i]),16)))

        payload=''.join(dmxarray)
        paquete=self.ip/self.udp/self.artnet/self.artdmx/payload

        send(paquete, verbose=0)


if __name__ == "__main__":

    camp = Camp('31.22.122.55')
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


