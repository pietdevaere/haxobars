#       artdmx.py
#       
#       Copyright 2011 J.A. Nache <nache.nache@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from scapy.packet import *
from scapy.fields import *

class ArtNet(Packet):
	name = "Art-Net"
	fields_desc = [
		StrFixedLenField('ID', 'Art-Net' , 8),
		XShortField("opcode", 0x0050),
		ByteField("protverh", 0),
		ByteField("protver", 14)
		]

class ArtDMX(Packet):
	name = "ArtDMX"
	fields_desc = [
		ByteField('sequence', 0),
		ByteField('physical', 0),
		ByteField('universe', 1),
		ByteField('subnet', 0),   #Segun la referencia, para los DMX-Hub
		XShortField('length', 0x0200)
		]
