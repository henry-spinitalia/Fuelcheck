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

        self.version = 2                      # Sempre pari a 2 per questa versione binaria

        # Definizione dei pacchetti binari
        self.s = struct.Struct('<BBHHHHBIBffHHHHHHHHHHBBH')  # Informazione di base

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
            self.s.size,				                                          # LEN
            0x02,                                                                 # VER
            int(self.imei[0:5]), int(self.imei[5:10]), int(self.imei[10:15]),     # IMEI
            self.driver,                                                          # DRVN
            self.event,                                                           # EVTN
            self.unixtime,                                                        # UTC_Unixtime
            self.sat,                                                             # GSAT
            self.lat,                                                             # LAT
            self.lon,                                                             # LON
            round(self.speed * 10),                                               # SPD
            round(self.gasoline_r * 10),                                          # Gasoline R
            round(self.gasoline_l * 10),                                          # Gasoline L
            round(self.gasoline_f * 10),                                          # Gasoline F
            round(self.vin * 10),                                                 # MBAT
            round(self.vbatt * 100),                                              # BBAT
            round(self.input_gasoline_r * 10),                                    # In gasoline R
            round(self.input_gasoline_l * 10),                                    # In gasoline L
            round(self.input_gasoline_f * 10),                                    # In gasoline F
            self.input_gasoline_tot,                                              # In gasoline TOT
            bitfield_input,                                                       # Inputs Bitpacked
            bitfield_output,                                                      # Outputs Bitpacked
            round(self.distance_travelled * 10)                                   # HSZZ
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

        # Per prima cosa usi unpack per trasformare il messaggio binario in una tupla di valori
        try:
            unpacked_data = self.s.unpack(input_message)
        except:
            raise ValueError("Lunghezza del pacchetto errata")

        # Ora ne controllo la lunghezza
        if unpacked_data[0] != self.s.size:
            raise ValueError("Lunghezza del pacchetto errata")

        # Poi assegni i vari elementi della tupla, agli attributi della classe BinaryProtocol ereditati
        # dal padre ControlUnit

        self.imei = "{:05d}{:05d}{:05d}".format(unpacked_data[2], unpacked_data[3], unpacked_data[4])
        self.driver = unpacked_data[5]
        self.event = unpacked_data[6]
        self.unixtime = unpacked_data[7]
        self.sat = unpacked_data[8]
        self.lat = unpacked_data[9]
        self.lon = unpacked_data[10]
        self.speed = unpacked_data[11] / 10.0
        self.gasoline_r = unpacked_data[12] / 10.0
        self.gasoline_l = unpacked_data[13] / 10.0
        self.gasoline_f = unpacked_data[14] / 10.0
        self.vin = unpacked_data[15] / 10.0
        self.vbatt = unpacked_data[16] / 100.0
        self.input_gasoline_r = unpacked_data[17] / 10.0
        self.input_gasoline_l = unpacked_data[18] / 10.0
        self.input_gasoline_f = unpacked_data[19] / 10.0
        self.input_gasoline_tot = unpacked_data[20]
        bitfield_input = unpacked_data[21]
        bitfield_output = unpacked_data[22]
        self.distance_travelled = unpacked_data[23] / 10.0

        # Decodifico il bitpack per gli input
        if  ((bitfield_input & BinaryProtocol.BIT_CUP_R) != 0):
            self.cup_r = ControlUnit.CUP_OPEN
        else:
            self.cup_r = ControlUnit.CUP_CLOSE

        if  ((bitfield_input & BinaryProtocol.BIT_CUP_L) != 0):
            self.cup_l = ControlUnit.CUP_OPEN
        else:
            self.cup_l = ControlUnit.CUP_CLOSE

        if  ((bitfield_input & BinaryProtocol.BIT_CUP_F) != 0):
            self.cup_f = ControlUnit.CUP_OPEN
        else:
            self.cup_f = ControlUnit.CUP_CLOSE

        if  ((bitfield_input & BinaryProtocol.BIT_ENGINE) != 0):
            self.engine = ControlUnit.ENGINE_ON
        else:
            self.engine = ControlUnit.ENGINE_OFF

        # Decodifico il bitpack per gli output
        if  ((bitfield_output & BinaryProtocol.BIT_ALARM) != 0):
            self.alarm = ControlUnit.ALARM_ARMED
        else:
            self.alarm = ControlUnit.ALARM_UNARMED

        if  ((bitfield_output & BinaryProtocol.BIT_CUP_LOCK) != 0):
            self.cup_lock = ControlUnit.CAPS_LOCKED
        else:
            self.cup_lock = ControlUnit.CAPS_UNLOCKED

        # Bisogna controllare tutti i parametri in ingresso
        try:
            self.check_values()
        except:
            raise

        return True

