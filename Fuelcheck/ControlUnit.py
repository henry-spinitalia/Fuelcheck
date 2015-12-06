# -*- coding: utf-8 -*-

import time
import math
import datetime
import calendar
import struct
import binascii


class ControlUnit():

    # Costanti per le variabili di stato
    CUP_OPEN = 1
    CUP_CLOSE = 0
    CUP_UNUSED = 2
    CUP_FAIL = 3
    ENGINE_ON = 1
    ENGINE_OFF = 0
    ALARM_ARMED = 1
    ALARM_UNARMED = 0
    CAPS_LOCKED = 1
    CAPS_UNLOCKED = 0

    # Input bits assignements
    BIT_CUP_R0 = 1 << 7
    BIT_CUP_R1 = 1 << 6
    BIT_CUP_L0 = 1 << 5
    BIT_CUP_L1 = 1 << 4
    BIT_CUP_F0 = 1 << 3
    BIT_CUP_F1 = 1 << 2
    BIT_ENGINE = 1 << 1

    # Output bits assignements
    BIT_ALARM = 1 << 7
    BIT_CUP_LOCK = 1 << 6

    # Set a value true:  table = table | testB
    # Set a value false: table = table & (~testC)
    # test: if ((table & testB & bitfield_length) != 0):

    def __init__(self):

        # Solo per il protocollo ASCII
        self.ascii_header = "A5"              # Sempre A5
        self.ascii_version = 1                # Sempre pari a 1 per la versione binaria

        # Solo per il protocollo BINARY
        self.binary_version = 2               # Sempre pari a 2 per la versione binaria

        # Codica binaria
        self.s_mex_1 = struct.Struct('<BBQHBIBffHHHHHHHHHHBBH')      # Messaggio di base
        self.s_mex_2 = struct.Struct('<BBQHBIBffHHHHHHHHHHBBHB')     # Messaggio con id distributore
        self.s_mex_3 = struct.Struct('<BBQHBIBffHHHHHHHHHHBBH130s')  # Messaggio con messaggio di testo
        self.s_mex_4 = struct.Struct('<BBQHBIBffHHHHHHHHHHBBH20s')   # Messaggio con targa

        # Variabili di stato della centralina
        self.imei = 123451234512345L          # 351535057249088 - 15 char len
        self.driver = 0                       # Id dell'autista
        self.event = 0                        # Id dell'evento
        self.unixtime = 0                     # Data dell'evento
        self.sat = 0                          # Numero di satelliti in vista
        self.lat = 0.0                        # Latitudine
        self.lon = 0.0                        # Longitude
        self.speed = 0.0                      # Velocità
        self.gasoline_r = 0.0                 # Quantità di carburante presente nel serbatoio destro
        self.gasoline_l = 0.0                 # Quantità di carburante presente nel serbatoio sinistro
        self.gasoline_f = 0.0                 # Quantità di carburante presente nel serbatoio frigo
        self.vin = 0.0                        # Tensione di alimentazione
        self.vbatt = 0.0                      # Tensione della batteria interna
        self.input_gasoline_r = 0.0           # Quantità di carburante immesso nel serbatoio destro
        self.input_gasoline_l = 0.0           # Quantità di carburante immesso nel serbatoio sinistro
        self.input_gasoline_f = 0.0           # Quantità di carburante immesso nel serbatoio frigo
        self.input_gasoline_tot = 0.0         # Quantità di carburante immesso dichiarata
        self.cup_r = ControlUnit.CUP_OPEN     # Tappo destro chiuso
        self.cup_l = ControlUnit.CUP_OPEN     # Tappo sinistro chiuso
        self.cup_f = ControlUnit.CUP_OPEN     # Tappo frigo chiuso
        self.engine = ControlUnit.ENGINE_OFF  # Stato del quadro di alimentazione
        self.unused_inputs = "UUUU"
        self.alarm = 0                        # Stato dell'allarme
        self.cup_lock = 0                     # Stato del blocco tappi
        self.unused_outputs = "UUUUUU"
        self.distance_travelled = 0.0         # Distanza percorsa dalla mezzanotte
        self.gas_station = 0                  # Id del distribuitore di benzina
        self.text_message = ""                # Messaggio chat
        self.plate = ""                       # Targa del mezzo in rifornimento
        self.output_packet = ""

    def check_values(self):

        if type(self.imei) is not long:
            raise TypeError("L'attributo imei deve essere un numero")
        if len(str(self.imei)) != 15:
            raise ValueError("L'attributo imei deve essere un numero di 15 cifre")
        if type(self.driver) is not int:
            raise TypeError("L'attributo driver deve essere un intero")
        if not 0 <= self.driver <= 9999:
            raise ValueError("L'attributo driver deve essere un intero positivo minore di 9999")
        if type(self.event) is not int:
            raise TypeError("L'attributo event deve essere un intero")
        if not 0 <= self.event <= 255:
            raise ValueError("L'attributo event deve essere un intero positivo minore di 255")
        if type(self.unixtime) is not int:
            raise TypeError("L'attributo unixtime deve essere un intero")
        if type(self.sat) is not int:
            raise TypeError("L'attributo sat deve essere un intero")
        if not 0 <= self.sat <= 255:
            raise ValueError("L'attributo sat deve essere un intero positivo minore di 255")
        if type(self.lat) is not float and type(self.lat) is not int:
            raise TypeError("L'attributo lat deve essere un numero intero o decimale")
        if not -90 <= self.lat <= 90:
            raise ValueError("L'attributo lat deve essere un numero intero o decimale compreso tra -90 e +90")
        if type(self.lon) is not float and type(self.lon) is not int:
            raise TypeError("L'attributo lon deve essere un numero intero o decimale")
        if not -180 <= self.lon <= 180:
            raise ValueError("L'attributo lon deve essere un numero intero o decimale compreso tra -180 e +180")
        if type(self.speed) is not float and type(self.speed) is not int:
            raise TypeError("L'attributo speed deve essere un numero intero o decimale")
        if not 0 <= self.speed <= 999.9:
            raise ValueError("L'attributo speed deve essere un numero intero o decimale positivo minore di 999.9")
        if type(self.gasoline_r) is not float and type(self.gasoline_r) is not int:
            raise TypeError("L'attributo gasoline_r deve essere un numero intero o decimale")
        if not 0 <= self.gasoline_r <= 999.9:
            raise ValueError("L'attributo gasoline_r deve essere un numero intero o decimale positivo minore di 999.9")
        if type(self.gasoline_l) is not float and type(self.gasoline_l) is not int:
            raise TypeError("L'attributo gasoline_l deve essere un numero intero o decimale")
        if not 0 <= self.gasoline_l <= 999.9:
            raise ValueError("L'attributo gasoline_l deve essere un numero intero o decimale positivo minore di 999.9")
        if type(self.gasoline_f) is not float and type(self.gasoline_f) is not int:
            raise TypeError("L'attributo gasoline_r deve essere un numero intero o decimale")
        if not 0 <= self.gasoline_f <= 999.9:
            raise ValueError("L'attributo gasoline_f deve essere un numero intero o decimale positivo minore di 999.9")
        if type(self.vin) is not float and type(self.vin) is not int:
            raise TypeError("L'attributo vin deve essere un numero intero o decimale")
        if not 0 <= self.vin <= 99.9:
            raise ValueError("L'attributo vin deve essere un numero intero o decimale positivo minore di 99.9")
        if type(self.vbatt) is not float and type(self.vbatt) is not int:
            raise TypeError("L'attributo vbatt deve essere un numero intero o decimale")
        if not 0 <= self.vbatt <= 9.99:
            raise ValueError("L'attributo vbatt deve essere un numero intero o decimale positivo minore di 9.99")
        if type(self.input_gasoline_r) is not float and type(self.input_gasoline_r) is not int:
            raise TypeError("L'attributo input_gasoline_r deve essere un numero intero o decimale")
        if not 0 <= self.input_gasoline_r <= 999.9:
            raise ValueError(
                "L'attributo input_gasoline_r deve essere un numero intero o decimale positivo minore di 999.9"
            )
        if type(self.input_gasoline_l) is not float and type(self.input_gasoline_l) is not int:
            raise TypeError("L'attributo input_gasoline_l deve essere un numero intero o decimale")
        if not 0 <= self.input_gasoline_l <= 999.9:
            raise ValueError(
                "L'attributo input_gasoline_l deve essere un numero intero o decimale positivo minore di 999.9"
            )
        if type(self.input_gasoline_f) is not float and type(self.input_gasoline_f) is not int:
            raise TypeError("L'attributo input_gasoline_f deve essere un numero intero o decimale")
        if not 0 <= self.input_gasoline_f <= 999.9:
            raise ValueError(
                "L'attributo input_gasoline_f deve essere un numero intero o decimale positivo minore di 999.9"
            )
        if type(self.input_gasoline_tot) is not int:
            raise TypeError("L'attributo input_gasoline_tot deve essere un numero intero")
        if not 0 <= self.input_gasoline_tot <= 9999:
            raise ValueError("L'attributo input_gasoline_tot deve essere un numero intero positivo minore di 9999")
        if type(self.cup_r) is not int:
            raise TypeError("L'attributo cup_r deve essere un numero intero")
        if self.cup_r not in (ControlUnit.CUP_CLOSE, ControlUnit.CUP_OPEN, ControlUnit.CUP_FAIL,
                              ControlUnit.CUP_UNUSED):
            raise ValueError("L'attributo cup_r deve essere pari a CUP_OPEN o CUP_CLOSE o CUP_FAIL o CUP_UNUSED")
        if type(self.cup_l) is not int:
            raise TypeError("L'attributo cup_l deve essere un numero intero")
        if self.cup_l not in (ControlUnit.CUP_CLOSE, ControlUnit.CUP_OPEN, ControlUnit.CUP_FAIL,
                              ControlUnit.CUP_UNUSED):
            raise ValueError("L'attributo cup_l deve essere pari a CUP_OPEN o CUP_CLOSE o CUP_FAIL o CUP_UNUSED")
        if type(self.cup_f) is not int:
            raise TypeError("L'attributo cup_f deve essere un numero intero")
        if self.cup_f not in (ControlUnit.CUP_CLOSE, ControlUnit.CUP_OPEN, ControlUnit.CUP_FAIL,
                              ControlUnit.CUP_UNUSED):
            raise ValueError("L'attributo cup_f deve essere pari a CUP_OPEN o CUP_CLOSE o CUP_FAIL o CUP_UNUSED")
        if type(self.engine) is not int:
            raise TypeError("L'attributo engine deve essere un numero intero")
        if self.engine not in (ControlUnit.ENGINE_OFF, ControlUnit.ENGINE_ON):
            raise ValueError("L'attributo engine deve essere pari a ENGINE_OFF o ENGINE_ON")
        if type(self.alarm) is not int:
            raise TypeError("L'attributo engine deve essere un numero intero")
        if self.alarm not in (ControlUnit.ALARM_UNARMED, ControlUnit.ALARM_ARMED):
            raise ValueError("L'attributo engine deve essere pari a ALARM_UNARMED o ALARM_ARMED")
        if type(self.cup_lock) is not int:
            raise TypeError("L'attributo engine deve essere un numero intero")
        if self.cup_lock not in (ControlUnit.CAPS_UNLOCKED, ControlUnit.CAPS_LOCKED):
            raise ValueError("L'attributo engine deve essere pari a CAPS_UNLOCKED o CAPS_LOCKED")
        if type(self.distance_travelled) is not float and type(self.distance_travelled) is not int:
            raise TypeError("L'attributo input_gasoline_f deve essere un numero intero o decimale")
        if not 0 <= self.distance_travelled <= 9999.9:
            raise ValueError(
                "L'attributo distance_travelled deve essere un numero intero o decimale positivo minore di 9999.9"
            )
        if type(self.gas_station) is not int:
            raise TypeError("L'attributo gas_station deve essere un intero")
        if not 0 <= self.gas_station <= 99:
            raise ValueError("Il valore dell'attributo gas_station deve essere compreso tra 0 e 99")

        if type(self.text_message) is not str:
            raise TypeError("L'attributo text_message deve essere una stringa unicode")
        if len(self.text_message) > 130:
            raise ValueError("La lunghezza dell'attributo text_message deve essere di 130 caratteri al massimo")

        if type(self.plate) is not str:
            raise TypeError("L'attributo plate deve essere una stringa unicode")
        if len(self.plate) > 20:
            raise ValueError("La lunghezza dell'attributo plate deve essere di 20 caratteri al massimo")

        return True

    def encode_ascii(self):
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
        if self.lat >= 0:
            lat_final = "{0:02.0f}{1:06.0f}N".format(temp[1], round(temp[0]*600000))
        else:
            lat_final = "{0:02.0f}{1:06.0f}S".format(temp[1], round(temp[0]*600000))

        # Converto la longitudine
        temp = math.modf(self.lon)
        if self.lon >= 0:
            lon_final = "{0:03.0f}{1:06.0f}E".format(temp[1], round(temp[0]*600000))
        else:
            lon_final = "{0:03.0f}{1:06.0f}W".format(temp[1], round(temp[0]*600000))

        # Converto il tappo destro
        if self.cup_r == ControlUnit.CUP_OPEN:
            cup_r_final = '1'
        elif self.cup_r == ControlUnit.CUP_CLOSE:
            cup_r_final = '0'
        elif self.cup_r == ControlUnit.CUP_UNUSED:
            cup_r_final = 'U'
        elif self.cup_r == ControlUnit.CUP_FAIL:
            cup_r_final = 'F'
        else:
            raise ValueError("Valore di cup_r diverso da OPEN/CLOSE/UNUSED/FAIL")

        # Converto il tappo sinistro
        if self.cup_l == ControlUnit.CUP_OPEN:
            cup_l_final = '1'
        elif self.cup_l == ControlUnit.CUP_CLOSE:
            cup_l_final = '0'
        elif self.cup_l == ControlUnit.CUP_UNUSED:
            cup_l_final = 'U'
        elif self.cup_l == ControlUnit.CUP_FAIL:
            cup_l_final = 'F'
        else:
            raise ValueError("Valore di cup_l diverso da OPEN/CLOSE/UNUSED/FAIL")

        # Converto il tappo frigo
        if self.cup_f == ControlUnit.CUP_OPEN:
            cup_f_final = '1'
        elif self.cup_f == ControlUnit.CUP_CLOSE:
            cup_f_final = '0'
        elif self.cup_f == ControlUnit.CUP_UNUSED:
            cup_f_final = 'U'
        elif self.cup_f == ControlUnit.CUP_FAIL:
            cup_f_final = 'F'
        else:
            raise ValueError("Valore di cup_f diverso da OPEN/CLOSE/UNUSED/FAIL")

        output_packet = self.ascii_header
        output_packet += "00"
        output_packet += "{0:02X}".format(1)
        output_packet += str(self.imei)
        output_packet += "{0:04d}".format(self.driver)
        output_packet += "{0:02X}".format(self.event)
        output_packet += time.strftime("%Y%m%d%H%M%S", s_time)
        output_packet += "{0:02d}".format(self.sat)
        output_packet += "{0:s}".format(lat_final)
        output_packet += "{0:s}".format(lon_final)
        output_packet += "{0:04.0f}".format(self.speed*10)
        output_packet += "{0:04.0f}".format(self.gasoline_r*10)
        output_packet += "{0:04.0f}".format(self.gasoline_l*10)
        output_packet += "{0:04.0f}".format(self.gasoline_f*10)
        output_packet += "{0:03.0f}".format(self.vin*10)
        output_packet += "{0:03.0f}".format(self.vbatt*100)
        output_packet += "{0:04.0f}".format(self.input_gasoline_r*10)
        output_packet += "{0:04.0f}".format(self.input_gasoline_l*10)
        output_packet += "{0:04.0f}".format(self.input_gasoline_f*10)
        output_packet += "{0:04.0f}".format(self.input_gasoline_tot)
        output_packet += "{0:s}".format(cup_r_final)
        output_packet += "{0:s}".format(cup_l_final)
        output_packet += "{0:s}".format(cup_f_final)
        output_packet += "{0:01d}".format(self.engine)
        output_packet += "UUUU"
        output_packet += "{0:01d}".format(self.alarm)
        output_packet += "{0:01d}".format(self.cup_lock)
        output_packet += "UUUUUU"
        output_packet += "{0:05.0f}".format(self.distance_travelled*10)


        # Caso di rifornimento
        if self.event == 0x13:
            output_packet += "{0:02d}".format(self.gas_station)
            # Calcolo la lunghezza e la inserisco in esadecimale
            output_packet = output_packet[0:2] + "{0:02X}".format(len(output_packet)) + output_packet[4:]

        # Caso di messaggio
        elif self.event == 0x14:
            output_packet += self.text_message + '$'
            # Calcolo la lunghezza e la inserisco in esadecimale
            output_packet = output_packet[0:2] + "{0:02X}".format(len(output_packet)) + output_packet[4:]

        # Caso di rifornimento cisterna
        elif self.event == 0x15:
            output_packet += self.plate + '$'
            # Calcolo la lunghezza e la inserisco in esadecimale
            output_packet = output_packet[0:2] + "{0:02X}".format(len(output_packet)) + output_packet[4:]

        else:
            if len(output_packet) != 121:
                return False

        # Calcolo la lunghezza e la inserisco in esadecimale
        output_packet = output_packet[0:2] + "{0:02X}".format(len(output_packet)) + output_packet[4:]

        self.output_packet = output_packet

        return True

    def decode_ascii(self, input_message):
        """Prende un messaggio codificato in ASCII e ne ricava tutte le variabili"""

        # Controllo l'header
        if input_message[0:2] != "A5":
            raise ValueError("Campo header errato ({0:2s} != A5)".format(input_message[0:2]))

        # Controllo la lunghezza del pacchetto
        if len(input_message) != int(input_message[2:4], 16):
            raise ValueError("Campo lunghezza stringa errato ({0:02X} != 0x79)".format(len(input_message)))

        # Controllo versione software
        if input_message[4:6] != "01":
            raise ValueError("Campo versione errato ({0:02X} != 01)".format(int(input_message[4:6])))

        # Controllo IMEI
        if not input_message[6:21].isdigit():
            raise ValueError("Campo IMEI non contiene solo numeri: ({0:15s})".format(input_message[6:21]))

        # Controllo Autista
        if not input_message[21:25].isdigit():
            raise ValueError("Campo Autista non contiene solo numeri: ({0:4s})".format(input_message[21:25]))

        # Controllo Evento (compreso tra 0 ed FF)
        if not 0 <= int(input_message[25:27], 16) <= 255:
            raise ValueError("Valore del campo Evento non compreso tra 0 e 255 ({0:2s})".format(input_message[25:27]))

        # Controllo Evento (compreso tra 0 ed FF)
        if input_message[25:27].isalnum() and input_message[25:27].islower():
            raise ValueError("Campo Evento non esadecimale maiuscolo: ({0:2s})".format(input_message[25:27]))

        # Controllo data YYYYMMDD
        if not input_message[27:35].isdigit():
            raise ValueError("Formato data non corretto presenza di caratteri: ({0:8s})".format(input_message[27:35]))
        try:
            datetime.datetime.strptime(input_message[27:35], '%Y%m%d')
        except ValueError:
            raise ValueError("Formato data non corretto: ({0:8s})".format(input_message[27:35]))

        # Controllo ora
        if not input_message[35:41].isdigit():
            raise ValueError("Formato ora non corretto presenza di caratteri: ({0:8s})".format(input_message[35:41]))
        try:
            datetime.datetime.strptime(input_message[35:41], '%H%M%S')
        except ValueError:
            raise ValueError("Formato ora non corretto: ({0:6s})".format(input_message[35:41]))

        # Controllo satelliti
        if not input_message[41:43].isdigit():
            raise ValueError(
                "Formato satelliti non corretto presenza di caratteri: ({0:2s})".format(input_message[41:43])
            )

        # Controllo latitudine
        if not input_message[43:51].isdigit():
            raise ValueError(
                "Formato latitudine non corretto presenza di caratteri: ({0:9s})".format(input_message[43:52])
            )
        if not 0 <= int(input_message[43:45], 10) <= 90:
            raise ValueError(
                "Formato latitudine non corretto fuori range +/-90°: ({0:9s})".format(input_message[43:52])
            )
        if int(input_message[45:47], 10) >= 60:
            raise ValueError("Formato latitudine non corretto fuori range > 59': ({0:9s})".format(input_message[43:52]))
        if input_message[51] != 'N' and input_message[51] != 'S':
            raise ValueError("Formato latitudine non corretto != N/S ({0:9s})".format(input_message[43:52]))

        # Controllo longitudine
        if not input_message[52:61].isdigit():
            raise ValueError(
                "Formato latitudine non corretto presenza di caratteri: ({0:10s})".format(input_message[52:62])
            )
        if not 0 <= int(input_message[52:55], 10) <= 180:
            raise ValueError(
                "Formato latitudine non corretto fuori range +/-180°: ({0:10s})".format(input_message[52:62])
            )
        if int(input_message[55:57], 10) >= 60:
            raise ValueError(
                "Formato latitudine non corretto fuori range > 59': ({0:10s})".format(input_message[52:62])
            )
        if input_message[61] != 'E' and input_message[61] != 'W':
            raise ValueError("Formato latitudine non corretto != E/W ({0:9s})".format(input_message[52:62]))

        # Controllo velocita'
        if not input_message[62:66].isdigit():
            raise ValueError(
                "Formato velocita' non corretto presenza di caratteri: ({0:4s})".format(input_message[62:66])
            )

        # Controllo litri serbatoio DX
        if not input_message[66:70].isdigit():
            raise ValueError(
                "Formato litri DX non corretto presenza di caratteri: ({0:4s})".format(input_message[66:70])
            )

        # Controllo litri serbatoio SX
        if not input_message[70:74].isdigit():
            raise ValueError(
                "Formato litri SX non corretto presenza di caratteri: ({0:4s})".format(input_message[70:74])
            )

        # Controllo litri serbatoio Frigo
        if not input_message[74:78].isdigit():
            raise ValueError(
                "Formato litri FR non corretto presenza di caratteri: ({0:4s})".format(input_message[74:78])
            )

        # Controllo tensione Batteria veicolo
        if not input_message[78:81].isdigit():
            raise ValueError(
                "Formato Tensione Vin non corretto presenza di caratteri: ({0:3s})".format(input_message[78:81])
            )

        # Controllo tensione Batteria interna
        if not input_message[81:84].isdigit():
            raise ValueError(
                "Formato Tensione Vbatt non corretto presenza di caratteri: ({0:3s})".format(input_message[81:84])
            )

        # Controllo litri immessi serbatoio DX
        if not input_message[84:88].isdigit():
            raise ValueError(
                "Formato litri immessi DX non corretto presenza di caratteri: ({0:4s})".format(input_message[84:88])
            )

        # Controllo litri immessi serbatoio SX
        if not input_message[88:92].isdigit():
            raise ValueError(
                "Formato litri immessi SX non corretto presenza di caratteri: ({0:4s})".format(input_message[88:92])
            )

        # Controllo litri immessi serbatoio Frigo
        if not input_message[92:96].isdigit():
            raise ValueError(
                "Formato litri immessi Frigo non corretto presenza di caratteri: ({0:4s})".format(input_message[92:96])
            )

        # Controllo litri Totali IN/OUT
        if not input_message[96:100].isdigit():
            raise ValueError(
                "Formato litri Totali IN/OUT non corretto presenza di caratteri: ({0:4s})".format(input_message[96:100])
            )

        # Controllo Tappo DX
        if not input_message[100] in ('1', '0', 'U', 'F'):
            raise ValueError(
                "Formato Tappo DX non corretto presenza di caratteri non validi: ({0:s})".format(input_message[100])
            )

        # Controllo Tappo SX
        if not input_message[101] in ('1', '0', 'U', 'F'):
            raise ValueError(
                "Formato Tappo SX non corretto presenza di caratteri non validi: ({0:s})".format(input_message[101])
            )

        # Controllo Tappo Frigo
        if not input_message[102] in ('1', '0', 'U', 'F'):
            raise ValueError(
                "Formato Tappo Frigo non corretto presenza di caratteri non validi: ({0:s})".format(input_message[102])
            )

        # Controllo Quadro
        if not input_message[103] in ('1', '0'):
            raise ValueError(
                "Formato Quadro non corretto presenza di caratteri non validi: ({0:s})".format(input_message[103])
            )

        # Controllo Allarme
        if not input_message[108] in ('1', '0'):
            raise ValueError(
                "Formato Allarme non corretto presenza di caratteri non validi: ({0:s})".format(input_message[108])
            )

        # Controllo Blocco tappi
        if not input_message[109] in ('1', '0'):
            raise ValueError(
                "Formato Blocco Tappi non corretto presenza di caratteri non validi: ({0:s})".format(input_message[109])
            )

        # Controllo Km percorsi
        if not input_message[116:121].isdigit():
            raise ValueError(
                "Formato Km percorsi non corretto presenza di caratteri: ({0:5s})".format(input_message[116:121])
            )

        self.imei = long(input_message[6:21])         # Inserisco l'IMEI verificato nella variabile imei
        self.driver = int(input_message[21:25])       # Inserisco l'autista verificato nella variabile driver
        self.event = int(input_message[25:27])        # Inserisco l'evento verificato nella variabile event

        # genero la stringa contenente YYYYMMDD e HHMMSS
        self.unixtime = calendar.timegm(datetime.datetime.strptime(input_message[27:41], "%Y%m%d%H%M%S").timetuple())
        self.sat = int(input_message[41:43])

        if input_message[51] == 'N':
            self.lat = float(input_message[43:45]) + float(input_message[45:51]) / 600000
        else:
            self.lat = -(float(input_message[43:45]) + float(input_message[45:51]) / 600000)
        if input_message[61] == 'E':
            self.lon = float(input_message[52:55]) + float(input_message[55:61]) / 600000
        else:
            self.lon = -(float(input_message[52:55]) + float(input_message[55:61]) / 600000)

        self.speed = (float(input_message[62:66])/10)
        self.gasoline_r = (float(input_message[66:70])/10)
        self.gasoline_l = (float(input_message[70:74])/10)
        self.gasoline_f = (float(input_message[74:78])/10)
        self.vin = (float(input_message[78:81])/10)
        self.vbatt = (float(input_message[81:84])/100)
        self.input_gasoline_r = (float(input_message[84:88])/10)
        self.input_gasoline_l = (float(input_message[88:92])/10)
        self.input_gasoline_f = (float(input_message[92:96])/10)
        self.input_gasoline_tot = int(input_message[96:100])

        if input_message[100] == '1':
            self.cup_r = ControlUnit.CUP_OPEN
        elif input_message[100] == '0':
            self.cup_r = ControlUnit.CUP_CLOSE
        elif input_message[100] == 'U':
            self.cup_r = ControlUnit.CUP_UNUSED
        elif input_message[100] == 'F':
            self.cup_r = ControlUnit.CUP_FAIL

        if input_message[101] == '1':
            self.cup_l = ControlUnit.CUP_OPEN
        elif input_message[101] == '0':
            self.cup_l = ControlUnit.CUP_CLOSE
        elif input_message[101] == 'U':
            self.cup_l = ControlUnit.CUP_UNUSED
        elif input_message[101] == 'F':
            self.cup_l = ControlUnit.CUP_FAIL

        if input_message[102] == '1':
            self.cup_f = ControlUnit.CUP_OPEN
        elif input_message[102] == '0':
            self.cup_f = ControlUnit.CUP_CLOSE
        elif input_message[102] == 'U':
            self.cup_f = ControlUnit.CUP_UNUSED
        elif input_message[102] == 'F':
            self.cup_f = ControlUnit.CUP_FAIL

        if input_message[103] == '1':
            self.engine = ControlUnit.ENGINE_ON
        elif input_message[103] == '0':
            self.engine = ControlUnit.ENGINE_OFF

        self.unused_inputs = str('UUUU')

        if input_message[108] == '1':
            self.alarm = ControlUnit.ALARM_ARMED
        elif input_message[108] == '0':
            self.alarm = ControlUnit.ALARM_UNARMED

        if input_message[109] == '1':
            self.cup_lock = ControlUnit.CAPS_LOCKED
        elif input_message[109] == '0':
            self.cup_lock = ControlUnit.CAPS_UNLOCKED

        self.unused_outputs = 'UUUUUU'

        self.distance_travelled = (float(input_message[116:121])/10)

        # Caso di Evento 13 Rifornimento
        if input_message[25:27] == '13':
            if not 0 <= int(input_message[121:123], 10) <= 99:
                raise ValueError("Valore del campo Rifornimento non compreso tra 0 e 255 ({0:2s})".format(input_message[121:123]))
            elif input_message[121:123].isalnum() and input_message[121:123].islower():
                raise ValueError("Campo Evento non esadecimale maiuscolo: ({0:2s})".format(input_message[121:123]))
            self.gas_station = int(input_message[121:123])

        # Caso di Evento 14 Rifornimento
        if input_message[25:27] == '14':
            self.text_message = input_message[121:]
            self.text_message = self.text_message.replace('$', '')

        # Caso di Evento 15 Rifornimento
        if input_message[25:27] == '15':
            self.plate = input_message[121:]
            self.plate = self.plate.replace('$', '')

        return True

    def encode_binary(self):
        """Prende una serie di variabili e ne crea un messaggio codificato in binario"""

        # Bisogna controllare tutti i parametri in ingresso
        try:
            self.check_values()
        except:
            raise

        # Creo il bitpack per gli input
        bitfield_input = 0

        # 00 - Unused [BIT_CUP_R BIT_CUP_RS]
        # 01 - Fail
        # 10 - Open
        # 11 - Close
        if self.cup_r == ControlUnit.CUP_OPEN:
            bitfield_input |= ControlUnit.BIT_CUP_R0
            bitfield_input &= ~ControlUnit.BIT_CUP_R1
        elif self.cup_r == ControlUnit.CUP_CLOSE:
            bitfield_input |= ControlUnit.BIT_CUP_R0
            bitfield_input |= ControlUnit.BIT_CUP_R1
        elif self.cup_r == ControlUnit.CUP_UNUSED:
            bitfield_input &= ~ControlUnit.BIT_CUP_R0
            bitfield_input &= ~ControlUnit.BIT_CUP_R1
        elif self.cup_r == ControlUnit.CUP_FAIL:
            bitfield_input &= ~ControlUnit.BIT_CUP_R0
            bitfield_input |= ControlUnit.BIT_CUP_R1
        else:
            raise ValueError("cup_r value != CUP_OPEN/CUP_CLOSE/CUP_UNUSED/CUP_FAIL")

        if self.cup_l == ControlUnit.CUP_OPEN:
            bitfield_input |= ControlUnit.BIT_CUP_L0
            bitfield_input &= ~ControlUnit.BIT_CUP_L1
        elif self.cup_l == ControlUnit.CUP_CLOSE:
            bitfield_input |= ControlUnit.BIT_CUP_L0
            bitfield_input |= ControlUnit.BIT_CUP_L1
        elif self.cup_l == ControlUnit.CUP_UNUSED:
            bitfield_input &= ~ControlUnit.BIT_CUP_L0
            bitfield_input &= ~ControlUnit.BIT_CUP_L1
        elif self.cup_l == ControlUnit.CUP_FAIL:
            bitfield_input &= ~ControlUnit.BIT_CUP_L0
            bitfield_input |= ControlUnit.BIT_CUP_L1
        else:
            raise ValueError("cup_l value != CUP_OPEN/CUP_CLOSE/CUP_UNUSED/CUP_FAIL")

        if self.cup_f == ControlUnit.CUP_OPEN:
            bitfield_input |= ControlUnit.BIT_CUP_F0
            bitfield_input &= ~ControlUnit.BIT_CUP_F1
        elif self.cup_f == ControlUnit.CUP_CLOSE:
            bitfield_input |= ControlUnit.BIT_CUP_F0
            bitfield_input |= ControlUnit.BIT_CUP_F1
        elif self.cup_f == ControlUnit.CUP_UNUSED:
            bitfield_input &= ~ControlUnit.BIT_CUP_F0
            bitfield_input &= ~ControlUnit.BIT_CUP_F1
        elif self.cup_f == ControlUnit.CUP_FAIL:
            bitfield_input &= ~ControlUnit.BIT_CUP_F0
            bitfield_input |= ControlUnit.BIT_CUP_F1
        else:
            raise ValueError("cup_l value != CUP_OPEN/CUP_CLOSE/CUP_UNUSED/CUP_FAIL")

        if self.engine == ControlUnit.ENGINE_ON:
            bitfield_input |= ControlUnit.BIT_ENGINE
        elif self.engine == ControlUnit.ENGINE_OFF:
            bitfield_input &= ~ControlUnit.BIT_ENGINE
        else:
            raise ValueError("engine value != ENGINE_ON/ENGINE_OFF")

        # Creo il bitpack per gli output
        bitfield_output = 0

        if self.alarm == ControlUnit.ALARM_ARMED:
            bitfield_output |= ControlUnit.BIT_ALARM
        elif self.alarm == ControlUnit.ALARM_UNARMED:
            bitfield_output &= ~ControlUnit.BIT_ALARM
        else:
            raise ValueError("alarm value != ALARM_ARMED/ALARM_UNARMED")

        if self.cup_lock == ControlUnit.CAPS_LOCKED:
            bitfield_output |= ControlUnit.BIT_CUP_LOCK
        if self.cup_lock == ControlUnit.CAPS_UNLOCKED:
            bitfield_output &= ~ControlUnit.BIT_CUP_LOCK
        else:
            raise ValueError("cup_lock value != CAPS_LOCKED/CAPS_UNLOCKED")

        # Se si tratta di un evento 13
        if self.event == 13:

            #  Valori di un pacchetto dati standard
            values = (
                self.s_mex_2.size,			                                          # LEN
                0x02,                                                                 # VER
                self.imei,                                                            # IMEI
                self.driver,                                                          # DRVN
                self.event,                                                           # EVTN
                self.unixtime,                                                        # UTC_Unixtime
                self.sat,                                                             # GSAT
                self.lat,                                                             # LAT
                self.lon,                                                             # LON
                int(round(self.speed * 10)),                                          # SPD
                int(round(self.gasoline_r * 10)),                                     # Gasoline R
                int(round(self.gasoline_l * 10)),                                     # Gasoline L
                int(round(self.gasoline_f * 10)),                                     # Gasoline F
                int(round(self.vin * 10)),                                            # MBAT
                int(round(self.vbatt * 100)),                                         # BBAT
                int(round(self.input_gasoline_r * 10)),                               # In gasoline R
                int(round(self.input_gasoline_l * 10)),                               # In gasoline L
                int(round(self.input_gasoline_f * 10)),                               # In gasoline F
                self.input_gasoline_tot,                                              # In gasoline TOT
                bitfield_input,                                                       # Inputs Bitpacked
                bitfield_output,                                                      # Outputs Bitpacked
                int(round(self.distance_travelled * 10)),                             # HSZZ
                self.gas_station                                                      # Station ID
            )
            packed_data = self.s_mex_2.pack(*values)

        elif self.event == 14:

            #  Valori di un pacchetto dati standard
            values = (
                self.s_mex_3.size,			                                          # LEN
                0x02,                                                                 # VER
                self.imei,                                                            # IMEI
                self.driver,                                                          # DRVN
                self.event,                                                           # EVTN
                self.unixtime,                                                        # UTC_Unixtime
                self.sat,                                                             # GSAT
                self.lat,                                                             # LAT
                self.lon,                                                             # LON
                int(round(self.speed * 10)),                                          # SPD
                int(round(self.gasoline_r * 10)),                                     # Gasoline R
                int(round(self.gasoline_l * 10)),                                     # Gasoline L
                int(round(self.gasoline_f * 10)),                                     # Gasoline F
                int(round(self.vin * 10)),                                            # MBAT
                int(round(self.vbatt * 100)),                                         # BBAT
                int(round(self.input_gasoline_r * 10)),                               # In gasoline R
                int(round(self.input_gasoline_l * 10)),                               # In gasoline L
                int(round(self.input_gasoline_f * 10)),                               # In gasoline F
                self.input_gasoline_tot,                                              # In gasoline TOT
                bitfield_input,                                                       # Inputs Bitpacked
                bitfield_output,                                                       # Outputs Bitpacked
                int(round(self.distance_travelled * 10)),                             # HSZZ
                self.text_message                                                     # Text message
            )
            packed_data = self.s_mex_3.pack(*values)

        elif self.event == 15:

            #  Valori di un pacchetto dati standard
            values = (
                self.s_mex_4.size,			                                          # LEN
                0x02,                                                                 # VER
                self.imei,                                                            # IMEI
                self.driver,                                                          # DRVN
                self.event,                                                           # EVTN
                self.unixtime,                                                        # UTC_Unixtime
                self.sat,                                                             # GSAT
                self.lat,                                                             # LAT
                self.lon,                                                             # LON
                int(round(self.speed * 10)),                                          # SPD
                int(round(self.gasoline_r * 10)),                                     # Gasoline R
                int(round(self.gasoline_l * 10)),                                     # Gasoline L
                int(round(self.gasoline_f * 10)),                                     # Gasoline F
                int(round(self.vin * 10)),                                            # MBAT
                int(round(self.vbatt * 100)),                                         # BBAT
                int(round(self.input_gasoline_r * 10)),                               # In gasoline R
                int(round(self.input_gasoline_l * 10)),                               # In gasoline L
                int(round(self.input_gasoline_f * 10)),                               # In gasoline F
                self.input_gasoline_tot,                                              # In gasoline TOT
                bitfield_input,                                                       # Inputs Bitpacked
                bitfield_output,                                                       # Outputs Bitpacked
                int(round(self.distance_travelled * 10)),                             # HSZZ
                self.plate                                                            # Plate
            )
            packed_data = self.s_mex_4.pack(*values)

        else:

            #  Valori di un pacchetto dati standard
            values = (
                self.s_mex_1.size,			                                          # LEN
                0x02,                                                                 # VER
                self.imei,                                                            # IMEI
                self.driver,                                                          # DRVN
                self.event,                                                           # EVTN
                self.unixtime,                                                        # UTC_Unixtime
                self.sat,                                                             # GSAT
                self.lat,                                                             # LAT
                self.lon,                                                             # LON
                int(round(self.speed * 10)),                                          # SPD
                int(round(self.gasoline_r * 10)),                                     # Gasoline R
                int(round(self.gasoline_l * 10)),                                     # Gasoline L
                int(round(self.gasoline_f * 10)),                                     # Gasoline F
                int(round(self.vin * 10)),                                            # MBAT
                int(round(self.vbatt * 100)),                                         # BBAT
                int(round(self.input_gasoline_r * 10)),                               # In gasoline R
                int(round(self.input_gasoline_l * 10)),                               # In gasoline L
                int(round(self.input_gasoline_f * 10)),                               # In gasoline F
                self.input_gasoline_tot,                                              # In gasoline TOT
                bitfield_input,                                                       # Inputs Bitpacked
                bitfield_output,                                                       # Outputs Bitpacked
                int(round(self.distance_travelled * 10))                              # HSZZ
            )
            packed_data = self.s_mex_1.pack(*values)

        print 'Original values:{0}'.format(values)
        print 'Original size  :{0}'.format(len(binascii.hexlify(packed_data)))
        print 'Format string  :{0}'.format(self.s_mex_1.format)
        print 'Uses           :{0}'.format(self.s_mex_1.size, 'bytes')
        print 'Packed Value   :{0}'.format(binascii.hexlify(packed_data).upper())

        self.output_packet = packed_data

        return True

    def decode_binary(self, input_message):
        """Prende un messaggio codificato in binario e ne ricava tutte le variabili"""

        # Trasformo i primi 50 bytes tramite unpack, che sono quelli fissi
        try:
            unpacked_data = self.s_mex_1.unpack(input_message[:50])
        except:
            raise ValueError("Lunghezza del pacchetto errata [Type 1]")

        # Nel caso si tratti dell'evento 13, il pacchetto si allunga di un byte
        if unpacked_data[4] == 13:
            try:
                unpacked_data = self.s_mex_2.unpack(input_message)
            except:
                raise ValueError("Lunghezza del pacchetto errata [Type 2]")

        # Nel caso si tratti dell'evento 14 o 15, il pacchetto si allunga di x bytes che sono una stringa
        elif unpacked_data[4] == 14:
            try:
                unpacked_data = self.s_mex_3.unpack(input_message)
            except:
                raise ValueError("Lunghezza del pacchetto errata [Type 3]")

        # Nel caso si tratti dell'evento 14 o 15, il pacchetto si allunga di x bytes che sono una stringa
        elif unpacked_data[4] == 15:
            try:
                unpacked_data = self.s_mex_4.unpack(input_message)
            except:
                raise ValueError("Lunghezza del pacchetto errata [Type 4]")

        self.imei = unpacked_data[2]
        self.driver = unpacked_data[3]
        self.event = unpacked_data[4]
        self.unixtime = unpacked_data[5]
        self.sat = unpacked_data[6]
        self.lat = unpacked_data[7]
        self.lon = unpacked_data[8]
        self.speed = unpacked_data[9] / 10.0
        self.gasoline_r = unpacked_data[10] / 10.0
        self.gasoline_l = unpacked_data[11] / 10.0
        self.gasoline_f = unpacked_data[12] / 10.0
        self.vin = unpacked_data[13] / 10.0
        self.vbatt = unpacked_data[14] / 100.0
        self.input_gasoline_r = unpacked_data[15] / 10.0
        self.input_gasoline_l = unpacked_data[16] / 10.0
        self.input_gasoline_f = unpacked_data[17] / 10.0
        self.input_gasoline_tot = unpacked_data[18]
        bitfield_input = unpacked_data[19]
        bitfield_output = unpacked_data[20]
        self.distance_travelled = unpacked_data[21] / 10.0

        # Se un rifornimento salvo anche l'id della stazione
        if self.event == 13:
            self.gas_station = unpacked_data[22]

        # Se un messaggio di testo, lo memorizzo
        if self.event == 14:
            self.text_message = unpacked_data[22].strip("\x00")

        # Se un rifornimento da cisterna, salvo la targa
        if self.event == 15:
            self.plate = unpacked_data[22].strip("\x00")

        # Decodifico il bitpack per gli input

        # 00 - Unused [BIT_CUP_R BIT_CUP_RS]
        # 01 - Fail
        # 10 - Open
        # 11 - Close
        if (bitfield_input & ControlUnit.BIT_CUP_R0) != 0 and (bitfield_input & ControlUnit.BIT_CUP_R1) == 0:
            self.cup_r = ControlUnit.CUP_OPEN
        elif (bitfield_input & ControlUnit.BIT_CUP_R0) != 0 and (bitfield_input & ControlUnit.BIT_CUP_R1) != 0:
            self.cup_r = ControlUnit.CUP_CLOSE
        elif (bitfield_input & ControlUnit.BIT_CUP_R0) == 0 and (bitfield_input & ControlUnit.BIT_CUP_R1) == 0:
            self.cup_r = ControlUnit.CUP_UNUSED
        elif (bitfield_input & ControlUnit.BIT_CUP_R0) == 0 and (bitfield_input & ControlUnit.BIT_CUP_R1) != 0:
            self.cup_r = ControlUnit.CUP_FAIL

        if (bitfield_input & ControlUnit.BIT_CUP_L0) != 0 and (bitfield_input & ControlUnit.BIT_CUP_L1) == 0:
            self.cup_l = ControlUnit.CUP_OPEN
        elif (bitfield_input & ControlUnit.BIT_CUP_L0) != 0 and (bitfield_input & ControlUnit.BIT_CUP_L1) != 0:
            self.cup_l = ControlUnit.CUP_CLOSE
        elif (bitfield_input & ControlUnit.BIT_CUP_L0) == 0 and (bitfield_input & ControlUnit.BIT_CUP_L1) == 0:
            self.cup_l = ControlUnit.CUP_UNUSED
        elif (bitfield_input & ControlUnit.BIT_CUP_L0) == 0 and (bitfield_input & ControlUnit.BIT_CUP_L1) != 0:
            self.cup_l = ControlUnit.CUP_FAIL

        if (bitfield_input & ControlUnit.BIT_CUP_F0) != 0 and (bitfield_input & ControlUnit.BIT_CUP_F1) == 0:
            self.cup_f = ControlUnit.CUP_OPEN
        elif (bitfield_input & ControlUnit.BIT_CUP_F0) != 0 and (bitfield_input & ControlUnit.BIT_CUP_F1) != 0:
            self.cup_f = ControlUnit.CUP_CLOSE
        elif (bitfield_input & ControlUnit.BIT_CUP_F0) == 0 and (bitfield_input & ControlUnit.BIT_CUP_F1) == 0:
            self.cup_f = ControlUnit.CUP_UNUSED
        elif (bitfield_input & ControlUnit.BIT_CUP_F0) == 0 and (bitfield_input & ControlUnit.BIT_CUP_F1) != 0:
            self.cup_f = ControlUnit.CUP_FAIL

        if (bitfield_input & ControlUnit.BIT_ENGINE) != 0:
            self.engine = ControlUnit.ENGINE_ON
        else:
            self.engine = ControlUnit.ENGINE_OFF

        # Decodifico il bitpack per gli output
        if (bitfield_output & ControlUnit.BIT_ALARM) != 0:
            self.alarm = ControlUnit.ALARM_ARMED
        else:
            self.alarm = ControlUnit.ALARM_UNARMED

        if (bitfield_output & ControlUnit.BIT_CUP_LOCK) != 0:
            self.cup_lock = ControlUnit.CAPS_LOCKED
        else:
            self.cup_lock = ControlUnit.CAPS_UNLOCKED

        # Bisogna controllare tutti i parametri in ingresso
        try:
            self.check_values()
        except:
            raise

        return True
