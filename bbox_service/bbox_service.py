# -*- coding: utf-8 -*-

# Questa classe al momento riceve in ingresso come parametro a linea di comando una stringa codificata secondo l'attuale
# protocollo, la comprime, la invia al server.

#  Referenze
# Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
# Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import struct
import binascii

class BBox():
	def __init__(self):
		self.IMEI = 351535057249088
		self.DriverCode = 2131
		self.Event = 1
		self.Date = "04/11/2015"
		self.Time = "20:00:00"
		self.GpsSat = 0
		self.GpsLat = "00 00.0000' N"
		self.GpsLong = "000 00.0000' E"
		self.GpsSpeed = 0.0
		self.TankRight = 9.4
		self.TankLeft = 8.8
		self.TankFridge = 8.6
		self.InputVoltage = 10.8
		self.BatteryVoltage = 4.18
		self.TankInRight = 0.0
		self.TankInLeft = 0.0
		self.TankInFridge = 0.0
		self.TankInDeclared = 0
		self.TankCupRightOpened = True
		self.TankCupLeftOpened = True
		self.TankCupFridgeOpened = True
		self.PowerOn = True
		self.Alarm = True
		self.TankCupsLock = True
		self.TotalKm = 0.0


class BBoxDatagramProtocol(DatagramProtocol):

	strings = [
		"Hello, world!",
		"What a fine day it is.",
		"Bye-bye!"
	]

	def __init__(self):

		self.Packets = 10
		self.bPacked = True

		# Pacchetto dati standard compresso, versione -> 2
		self.s = struct.Struct('<BBHHHHBIBffHHHHHHHHHHBBH')

	def pack_data(self):

		if not self.bPacked:

			data = "A5"
			data += "79"
			data += "01"
			data += "3515350572490884938"
			data += "00"
			data += "20151019192307"
			data += "0000000000N"
			data += "000000000E"
			data += "0000011400920098109414"
			data += "00000000000000000001FUUU10UUUUUU00000"
			return data

		else:

			#  Valori di un pacchetto dati standard
			values = (
				0x79,                    # LEN
				0x02,                    # VER
				35153,  50572, 49088,    # IMEI
				0xFAFA,                  # DRVN
				0x12,                    # EVTN
				1447341026,              # UTC_Unixtime
				07,                      # GSAT
				43.1232321,              # LAT
				12.32133213,             # LON
				1231,                    # SPD
				5001, 3002, 1003,        # Gasoline LRF
				241,                     # MBAT
				624,                     # BBAT
				6001, 4002, 2003,        # In gasoline LRF
				1200,                    # In gasoline TOT
				0xAF,                    # Inputs Bitpacked
				0x0F,                    # Outputs Bitpacked
				12345                    # HSZZ
			)
			packed_data = self.s.pack(*values)

			print 'Original values:{}'.format(values)
			print 'Original size  :{}'.format(len(binascii.hexlify(packed_data)))
			print 'Format string  :{}'.format(self.s.format)
			print 'Uses           :{}'.format(self.s.size, 'bytes')
			print 'Packed Value   :{}'.format(binascii.hexlify(packed_data).upper())

			return packed_data

	def startProtocol(self):
		self.transport.connect('127.0.0.1', 8000)
		self.sendDatagram()

	def sendDatagram(self):
		if self.Packets >= 0:
			self.transport.write(self.pack_data())
			self.Packets -= 1
		else:
			reactor.stop()

	def datagramReceived(self, datagram, host):
		print 'Datagram received: ', repr(datagram)
		self.sendDatagram()


if __name__ == '__main__':
	reactor.listenUDP(0, BBoxDatagramProtocol())
	reactor.run()