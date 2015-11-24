# -*- coding: utf-8 -*-
from ControlUnit import ControlUnit
import time
import math

class AsciiProtocol(ControlUnit):
    """Classe per la codifica e decodifica del protocollo ASCII attualmente implementato"""

    def __init__(self):

        ControlUnit.__init__(self)

        self.header = "A5"                    # Always A5
        self.version = 1

    def encode(self):
        """Prende una serie di variabili e ne crea un messaggio codificato in ASCII"""

        # Bisogna controllare tutti i parametri in ingresso
        try:
            self.check_values()
        except:
            raise

        # Converto la data in struct_time UTC
        s_time = time.gmtime(self.unixtime)

        # Converto la latitudine
        temp = math.modf(self.lat)
        if self.lat > 0:
            lat_final = "{:02.0f}{:06.0f}N".format(temp[1],round(temp[0]*600000))
        else:
            lat_final = "{:02.0f}{:06.0f}S".format(temp[1],round(temp[0]*600000))
        # Converto la longitudine
        temp = math.modf(self.lon)
        if self.lon > 0:
            lon_final = "{:03.0f}{:06.0f}E".format(temp[1],round(temp[0]*600000))
        else:
            lon_final = "{:03.0f}{:06.0f}W".format(temp[1],round(temp[0]*600000))

        output_packet = self.header
        output_packet += "00"
        output_packet += "{:02X}".format(1)
        output_packet += self.imei
        output_packet += "{:04d}".format(self.driver)
        output_packet += "{:02X}".format(self.event)
        output_packet += time.strftime("%Y%m%d%H%M%S", s_time)
        output_packet += "{:02d}".format(self.sat)
        output_packet += "{:s}".format(lat_final)
        output_packet += "{:s}".format(lon_final)
        output_packet += "{:04.0f}".format(self.speed*10)
        output_packet += "{:04.0f}".format(self.gasoline_r*10)
        output_packet += "{:04.0f}".format(self.gasoline_l*10)
        output_packet += "{:04.0f}".format(self.gasoline_f*10)
        output_packet += "{:03.0f}".format(self.vin*10)
        output_packet += "{:03.0f}".format(self.vbatt*100)
        output_packet += "{:04.0f}".format(self.input_gasoline_r*10)
        output_packet += "{:04.0f}".format(self.input_gasoline_l*10)
        output_packet += "{:04.0f}".format(self.input_gasoline_f*10)
        output_packet += "{:04.0f}".format(self.input_gasoline_tot)
        output_packet += "{:01d}".format(self.cup_r)
        output_packet += "{:01d}".format(self.cup_l)
        output_packet += "{:01d}".format(self.cup_f)
        output_packet += "{:01d}".format(self.engine)
        output_packet += "UUUU"
        output_packet += "{:01d}".format(self.alarm)
        output_packet += "{:01d}".format(self.cup_lock)
        output_packet += "UUUUUU"
        output_packet += "{:05.0f}".format(self.distance_travelled*10)

        if len(output_packet) != 121:
            return False

        # Calcolo la lunghezza e la inserisco in esadecimale
        output_packet = output_packet[0:2] + "{:02X}".format(len(output_packet)) + output_packet[4:]

        self.output_packet = output_packet

        return True

    def decode(self, input_message):
        """Prende un messaggio codificato in ASCII e ne ricava tutte le variabili"""

        return True

