# -*- coding: utf-8 -*-

# Questa classe rimane in ascolto su una porta, per messaggi codificati, li decomprime, li invia al MULE, riceve le
# risposte e le restituisce alle centraline
#
#        +------+                   +------------+                   +------+
#        | BBox |------------------>|     Me     |------------------>| MULE |
#        |      |<------------------|            |<------------------|      |
#        +------+                   +------------+                   +------+
#


from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import struct


class BBoxDecoder(DatagramProtocol):
	"""Riceve un messaggio compresso dalle centraline e lo spedisce al server"""

	def __init__(self):
		# Definizione del pacchetto binario
		self.s = struct.Struct('<BBHHHHBIBffHHHHHHHHHHBBH')

	def datagramReceived(self, data, (host, port)):
		# Evento: mi è appena arrivato un pacchetto binario dalle centraline, intanto lo devo interpretare
		print("received {} from {}:{}".format(data, host, port))
		self.transport.write("A50006", (host, port))

if __name__ == '__main__':
	reactor.listenUDP(9123, BBoxDecoder())
	reactor.run()
