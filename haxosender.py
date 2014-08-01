from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep
from random import randrange

class Effect:
    def __init__(self, kind):
        self.kind = kind

class Dimmer(Effect):
    def __init__(self, light, bank = None, targets = None, speed = 1):
        Effect.__init__(self, 'dimmer')
        self.light = light
        self.speed = speed
        self.bank = bank
        if targets == None:
            self.targets = self.light.default_values()
        else:
            self.targets = targets
    
    def set_targets(self, targets):
        self.targets = targets

    def set_speed(self, speed):
        self.speed = speed


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
    def default_values(self):
        return [255, 0, 0, 0, 255, 0, 0, 0, 0, 0]
    def __init__(self, adr):
        Light.__init__(self, adr, 10, 'city')
        self.values = self.default_values()
 
    def set_strobe(self, val):
        self.values[7] = val
    

class Bar(Light):
    def default_values(self):
        return  [12, 255, 0,
                125, 125, 125, 125,
                125, 125, 125, 125,
                125, 125, 125, 125,
                125, 125, 125, 125]

    def __init__(self, adr, width=19):
        Light.__init__(self, adr, width, 'bar')
        self.values = self.default_values()


    def rgba(self, rgbaArray, block = None):
        assert len(rgbaArray) == 4
        if block == None:
            for i in range(4):
                self.rgba(rgbaArray, i)
        else:
            self.values[3 + 4*block: 3 + 4*block + 4] = rgbaArray

    def read_block(self, block):
        return self.values[3 + 4*block: 3 + 4*block + 4]

class Camp:
    def __init__(self, dst, port = 6454):
        self.lights = set()
        self.effects = {}
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
    
    def add_dimmer(self, soft):
        light, bank = self.resTable.lookup(soft)
        newDimmer = Dimmer(light, bank)
        self.effects[soft] = newDimmer

    def random_dimmer(self, soft):
        light, bank = self.resTable.lookup(soft)
        newDimmer = Dimmer(light, bank)
        self.effects[soft] = newDimmer
        if light.kind == 'bar':
            targets = []
            for i in range(4):
                targets.append(randrange(0,256))
            self.set_dimmer_target(soft, targets)

        
    def set_dimmer_target(self, soft, targets):
        self.effects[soft].set_targets(targets)

    def set_dimmer_speed(self, soft, speed):
        self.effects[soft].set_speed(speed)

    def do_effects(self):
        finished = []
        for soft in self.effects.keys():
            effect = self.effects[soft]
            if effect.kind == 'dimmer':
                vals = self.read_light(soft)
                done = 1
                for i in range(min(len(vals), len(effect.targets))):
                    if vals[i] < effect.targets[i]:
                        vals[i] += 1
                    elif vals[i] > effect.targets[i]:
                        vals[i] -= 1
                    if vals[i] != effect.targets[i]:
                        done = 0
                self.set_light(soft, vals)
                if done == 1:
                    del self.effects[soft]
                    finished.append((soft, effect))
        return finished
                

    def read_light(self, soft):
        light, block = self.resTable.lookup(soft)
        if light.kind == 'bar':
            return light.read_block(block)


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
        self.artdmx.setfieldval("length", len(universe))
        dmxarray=[]
        for i in range(len(universe)):
            dmxarray.append(chr(int(hex(universe[i]),16)))

        payload=''.join(dmxarray)
        paquete=self.ip/self.udp/self.artnet/self.artdmx/payload

        send(paquete, verbose=0)

if __name__ == "melons":

    camp = Camp("31.22.123.224")
    for i in range(20):
        camp.add_light('bar', 1 + i*19, i*4)

    camp.set_light(14, (0, 255, 0, 0))
    camp.transmit()

if __name__ == "boobs":
    camp = Camp("31.22.123.224")
    for i in range(20):
        camp.add_light('bar', 1 + i*19, i*4)

    while True:
        for soft in range(80):
            camp.set_light(soft, (255, 0, 0, 0))
        camp.transmit()
        sleep(0.01)
        
        for soft in range(80):
            camp.set_light(soft, (0, 0, 255, 0))
        camp.transmit()
        sleep(0.01)

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


if __name__ == "tits":

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


