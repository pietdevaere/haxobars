from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep
from random import randrange

class Effect:
    """Special effect superclass"""
    def __init__(self, kind):
        self.kind = kind

class Dimmer(Effect):
    """Make a light fade slowely to the targets"""
    def __init__(self, light, bank = None, targets = None, speed = 1):
        """Set up a dimmer"""
        Effect.__init__(self, 'dimmer')
        self.light = light
        self.speed = speed
        self.counter = 0
        self.bank = bank
        if targets == None:
            self.targets = self.light.default_values()
        else:
            self.targets = targets
    
    def set_targets(self, targets):
        """Set the values the channels should fade to"""
        self.targets = targets

    def set_speed(self, speed):
        """Set the speed of the effect, the higher the speed, the slower the effect"""
        self.speed = speed

    def do(self):
        """Perform one step of fading
        returns 1 if the fading is done (eg. the targets are reached)
        returns 0 otherwise"""
        self.counter += 1
        if self.counter >= self.speed:
            self.counter = 0
            if self.light.kind == 'bar':
                vals = self.light.read_block(self.bank)
                done = 1
                for i in range(min(len(vals), len(self.targets))):
                    if vals[i] < self.targets[i]:
                        vals[i] += 1
                    elif vals[i] > self.targets[i]:
                        vals[i] -= 1
                    if vals[i] != self.targets[i]:
                        done = 0
                self.light.rgba(vals, self.bank)
                return done

class Mapper:
    """Map soft adresses to dmx base adresses and banks"""
    def __init__(self):
        """Generate an emtpy table on initialisation"""
        self.table = {}

    def add(self, soft, adr, block = None):
        """Add an element the the table"""
        self.table[soft] = [adr, block]

    def lookup(self, soft):
        """Do a forward lookup
        Find the dmx base adress and block of a given softadress"""
        return self.table[soft]

class Light:
    """Superclass for the different type of lights"""
    def __init__(self, adr, width, kind = None):
        self.adr = adr
        self.width = width
        self.kind = kind
        self.values = [0 for i in range(width)]

    def __repr__(self):
        return(str(self.values))

class Eurospot(Light):
    """Class for the eurospott of bernadski"""
    channel_map = ('R', 'G', 'B', 'MACRO', 'speed/strobe', 'MODE')
    def default_values(self):
        return [255, 255, 255, 0, 0, 0]

    def __init__(self, adr):
        Light.__init__(self, adr, 6, 'eurospot')
        self.values = self.default_values()

    def rgb(self, mix):
        self.values[0:3] = mix

class City(Light):
    """Class for the city floodlights"""
    def default_values(self):
        return [255, 0, 0, 0, 255, 0, 0, 0, 0, 0]
    def __init__(self, adr):
        Light.__init__(self, adr, 10, 'city')
        self.values = self.default_values()
 
    def set_strobe(self, val):
        self.values[7] = val
    

class Bar(Light):
    """Class for the bar lights"""
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
        """Set the given block of the light to the given rgba code
        will set all blocks if no block is specified"""
        assert len(rgbaArray) == 4
        if block == None:
            for i in range(4):
                self.rgba(rgbaArray, i)
        else:
            self.values[3 + 4*block: 3 + 4*block + 4] = rgbaArray

    def read_block(self, block):
        """Read back the value of a block"""
        return self.values[3 + 4*block: 3 + 4*block + 4]

class Camp:
    """Superclass for the controller, keeps track of all the lights and effects"""
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
        """Add a light to the camp"""
        if kind == 'bar':
            newLight = Bar(adr)
            self.lights.add(newLight)
            for i in range(4):
                self.resTable.add(soft + i, newLight, i)
        elif kind == 'city':
            newLight = City(adr)
            self.lights.add(newLight)
            self.resTable.add(soft, newLight)
        elif kind == 'eurospot':
            newLight = Eurospot(adr)
            self.lights.add(newLight)
            self.resTable.add(soft, newLight)
        return newLight
    
    def add_dimmer(self, soft):
        """Add a dimmer to the camp"""
        light, bank = self.resTable.lookup(soft)
        newDimmer = Dimmer(light, bank)
        self.effects[soft] = newDimmer

    def random_dimmer(self, soft):
        """Generate a dimmer to fade to a random value"""
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
        """execute all the effects once"""
        finished = []
        for soft in self.effects.keys():
            effect = self.effects[soft]
            done = effect.do()
            if done == 1:
                del self.effects[soft]
                finished.append((soft, effect))
        return finished
                

    def read_light(self, soft):
        """read back the current state of a given light"""
        light, block = self.resTable.lookup(soft)
        if light.kind == 'bar':
            return light.read_block(block)


    def set_light(self, soft, val):
        """set the given softadress to the given collorvalue"""
        light, block = self.resTable.lookup(soft)
        if light.kind == 'bar':
            light.rgba(val, block)
        elif light.kind == 'city':
            light.set_strobe(val)
        elif light.kind == 'eurospot':
            light.rgb(val)

    def find_light(self, soft):
        """return the adress and bank of a given softadress"""
        return self.resTable.lookup(soft)

    def get_size(self):
        """calculate the size of the universe"""
        for light in self.lights:
            if light.adr + light.width > self.size:
                self.size = light.adr + light.width

    def transmit(self):
        """Create the dmx data, and send out the universe"""
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

class Sender:
    """Simple class to send basic dmx packages"""
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


