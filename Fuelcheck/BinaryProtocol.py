# -*- coding: utf-8 -*-
# -*- test-case-name: Fuelcheck.test.test_AsciiProtocol -*-
from ControlUnit import ControlUnit
import struct

class BinaryProtocol(ControlUnit):
	"""Classe per la codifica e decodifica del protocollo binario attualmente implementato
	"""

	def __init__(self):

		ControlUnit.__init__(self)

		# Definizione del pacchetto binario
		self.s = struct.Struct('<BBHHHHBIBffHHHHHHHHHHBBH')

	def encode(self, imei, driver, event, unixtime, sat, lat, lon, speed, gasoline_r, gasoline_l, gasoline_f, vin,
				vbatt, input_gasoline_r, input_gasoline_l, input_gasoline_f, input_gasoline_tot, cup_r, cup_l, cup_f,
				engine, alarm, cup_lock, distance_travelled):
		"""Prende un pacchetto codificato, e lo spezza secondo le sue componenti"""

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

	def decode(self, input_message):
		"""Prende un messaggio codificato e lo spezza in tutte le sue parti"""

		return True
