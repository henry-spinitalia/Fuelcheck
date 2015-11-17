# -*- coding: utf-8 -*-

__author__ = 'Henry'


class ControlUnit():

	CUP_OPEN = 1
	CUP_CLOSE = 0
	ENGINE_ON = 1
	ENGINE_OFF = 0
	ALARM_ARMED = 1
	ALARM_UNARMED = 0
	CAPS_LOCKED = 1
	CAPS_UNLOCKED = 0

	def __init__(self):

		self.header = "A5"             # Always A5
		self.len = 0                   # Nomally 121 + optional data len
		self.version = 1               # Always 1 for ascii
		self.imei = "000000000000000"  # 351535057249088 - 15 char len
		self.driver = 0                # Id dell'autista
		self.event = 0                 # Id dell'evento
		self.date_day = 0              # Giorno dell'evento
		self.date_month = 0            # Mese dell'evento
		self.date_year = 0             # Anno dell'evento
		self.time_hour = 0             # Ora dell'evento
		self.time_minute = 0           # Minuti dell'evento
		self.time_second = 0           # Secondi dell'evento
		self.sat = 0                   # Numero di satelliti in vista
		self.lat = 0.0                 # Latitudine
		self.lon = 0.0                 # Longitude
		self.speed = 0.0               # Velocità
		self.gasoline_r = 0.0          # Quantità di carburante presente nel serbatoio destro
		self.gasoline_l = 0.0          # Quantità di carburante presente nel serbatoio sinistro
		self.gasoline_f = 0.0          # Quantità di carburante presente nel serbatoio frigo
		self.vin = 0.0                 # Tensione di alimentazione
		self.vbatt = 0.0               # Tensione della batteria interna
		self.input_gasoline_r = 0.0    # Quantità di carburante immesso nel serbatoio destro
		self.input_gasoline_l = 0.0    # Quantità di carburante immesso nel serbatoio sinistro
		self.input_gasoline_f = 0.0    # Quantità di carburante immesso nel serbatoio frigo
		self.input_gasoline_tot = 0.0  # Quantità di carburante immesso dichiarata
		self.cup_r = self.CUP_OPEN     # Tappo destro chiuso
		self.cup_l = self.CUP_OPEN     # Tappo sinistro chiuso
		self.cup_f = self.CUP_OPEN     # Tappo frigo chiuso
		self.engine = self.ENGINE_OFF  # Stato del quadro di alimentazione
		self.unused_inputs = "0000"
		self.alarm = 0                 # Stato dell'allarme
		self.cup_lock = 0              # Stato del blocco tappi
		self.unused_outputs = "000000"
		self.distance_travelled = 0.0  # Distanza percorsa dalla mezzanotte
