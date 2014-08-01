from artdmx import ArtNet, ArtDMX
from scapy.all import *
from itertools import chain
from time import sleep
from haxosender import Sender

# universe = [ 255,255,64, 255,255,64, 255,255,64, 255,255,64 ]
universe = [ 255,172,0, 255,172,0, 255,172,0, 255,172,0 ]

#   br  fl rgba rgba rgba
#12 255 0 

def unroll(array):
    outArray=[]
    for i in range(len(array)/4):
        if i%4==0:
            outArray.extend([12,255,0])
        outArray.extend(array[i*4:((i+1)*4)])
    #print "--"
    #print outArray
    return outArray

bgColor = [0,0,255,0]
fgColor = [255,0,0,0]
#fgColor = [0,0,0,0]
#bgColor = [255,255,255,0]

if __name__ == "__main__":
    bars = Sender('31.22.122.55')
    bars.fake = False

    numSegments = 80

    blink = True

    while True:
        for y in range(0,1):
            for j in range(0,numSegments):
                array=[]
                for i in range(0,numSegments):
                    if i%20 == j%20:
                        array.extend(bgColor)
                    else:
                        array.extend(fgColor)
                bars.send(unroll(array))
                sleep(0.05)
        if blink:
            for x in range(0,3):
                array=[]
                for j in range(0,numSegments):
                    array.extend(bgColor)
                bars.send(unroll(array))
                sleep(0.1)

                array=[]
                for j in range(0,numSegments):
                    array.extend(fgColor)
                bars.send(unroll(array))
                sleep(0.1)
                    

                
