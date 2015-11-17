# -*- coding: utf-8 -*-
# -*- test-case-name: Fuelcheck.test.test_AsciiProtocol -*-
from ControlUnit import ControlUnit


class AsciiProtocol(ControlUnit):
	"""Classe per la codifica e decodifica del protocollo ASCII attualmente implementato
	"""

	def __init__(self):

		ControlUnit.__init__(self)

	def encode(self, imei, driver, event, unixtime, sat, lat, lon, speed, gasoline_r, gasoline_l, gasoline_f, vin,
				vbatt, input_gasoline_r, input_gasoline_l, input_gasoline_f, input_gasoline_tot, cup_r, cup_l, cup_f,
				engine, alarm, cup_lock, distance_travelled):
		"""Prende una serie di variabili e ne crea un messaggio codificato in ASCII"""

		output_packet = "A5"

		return output_packet

	def decode(self, input_message):
		"""Prende un messaggio codificato in ASCII e ne ricava tutte le variabili"""

		return True

