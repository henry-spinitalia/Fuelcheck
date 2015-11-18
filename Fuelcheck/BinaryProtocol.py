# -*- coding: utf-8 -*-
from ControlUnit import ControlUnit
import struct
import binascii


class BinaryProtocol(ControlUnit):
	"""Classe per la codifica e decodifica del protocollo binario attualmente implementato"""

	# Input bits assignements
	BIT_CUP_R = 1 << 7
	BIT_CUP_L = 1 << 6
	BIT_CUP_F = 1 << 5
	BIT_ENGINE = 1 << 4

	# Output bits assignements
	BIT_ALARM = 1 << 7
	BIT_CUP_LOCK = 1 << 6

	# Set a value true:  table = table | testB
	# Set a value false: table = table & (~testC)
	# test: if ((table & testB & bitfield_length) != 0):

	def __init__(self):

		ControlUnit.__init__(self)

		# Definizione del pacchetto binario
		self.s = struct.Struct('<BBHHHHBIBffHHHHHHHHHHBBH')

	def encode(self):
		"""Prende una serie di variabili e ne crea un messaggio codificato in binario"""

		# Bisogna controllare tutti i parametri in ingresso
		try:
			self.check_values()
		except:
			raise

		# Creo il bitpack per gli input
		bitfield_input = 0
		if self.cup_r == ControlUnit.CUP_OPEN:
			bitfield_input |= BinaryProtocol.BIT_CUP_R
		if self.cup_l == ControlUnit.CUP_OPEN:
			bitfield_input |= BinaryProtocol.BIT_CUP_L
		if self.cup_f == ControlUnit.CUP_OPEN:
			bitfield_input |= BinaryProtocol.BIT_CUP_F
		if self.engine == ControlUnit.ENGINE_ON:
			bitfield_input |= BinaryProtocol.BIT_ENGINE

		# Creo il bitpack per gli output
		bitfield_output = 0
		if self.alarm == ControlUnit.ALARM_ARMED:
			bitfield_output |= BinaryProtocol.BIT_ALARM
		if self.cup_lock == ControlUnit.CAPS_LOCKED:
			bitfield_output |= BinaryProtocol.BIT_CUP_LOCK

		#  Valori di un pacchetto dati standard
		values = (
			0x79, 					                                              # LEN
			0x02,                                                                 # VER
			int(self.imei[0:5]), int(self.imei[5:10]), int(self.imei[10:15]),     # IMEI
			self.driver,                                                          # DRVN
			self.event,                                                           # EVTN
			self.unixtime,                                                        # UTC_Unixtime
			self.sat,                                                             # GSAT
			self.lat,                                                             # LAT
			self.lon,                                                             # LON
			self.speed,                                                           # SPD
			self.gasoline_r, self.gasoline_l, self.gasoline_f,                    # Gasoline LRF
			self.vin,                                                             # MBAT
			self.vbatt,                                                           # BBAT
			self.input_gasoline_r, self.input_gasoline_l, self.input_gasoline_f,  # In gasoline LRF
			self.input_gasoline_tot,                                              # In gasoline TOT
			bitfield_input,                                                       # Inputs Bitpacked
			bitfield_output,                                                      # Outputs Bitpacked
			self.distance_travelled                                               # HSZZ
		)
		packed_data = self.s.pack(*values)

		print 'Original values:{}'.format(values)
		print 'Original size  :{}'.format(len(binascii.hexlify(packed_data)))
		print 'Format string  :{}'.format(self.s.format)
		print 'Uses           :{}'.format(self.s.size, 'bytes')
		print 'Packed Value   :{}'.format(binascii.hexlify(packed_data).upper())

		self.output_packet = packed_data

		return True

	def decode(self, input_message):
		"""Prende un messaggio codificato in binario e ne ricava tutte le variabili"""

		return True
