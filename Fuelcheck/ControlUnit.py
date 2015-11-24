# -*- coding: utf-8 -*-


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

        self.imei = "000000000000000"         # 351535057249088 - 15 char len
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
        self.unused_inputs = "0000"
        self.alarm = 0                        # Stato dell'allarme
        self.cup_lock = 0                     # Stato del blocco tappi
        self.unused_outputs = "000000"
        self.distance_travelled = 0.0         # Distanza percorsa dalla mezzanotte
        self.output_packet = ""

    def check_values(self):

        if len(self.imei) != 15:
            raise ValueError("L'attributo imei deve essere una stringa numerica lunga 15 caratteri")
        if not self.imei.isdigit():
            raise TypeError("L'attributo imei deve essere una stringa numerica")
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
        if self.cup_r is not ControlUnit.CUP_CLOSE and self.cup_r is not ControlUnit.CUP_OPEN:
            raise ValueError("L'attributo cup_r deve essere pari a CUP_OPEN o CUP_CLOSE")
        if type(self.cup_l) is not int:
            raise TypeError("L'attributo cup_l deve essere un numero intero")
        if self.cup_l is not ControlUnit.CUP_CLOSE and self.cup_l is not ControlUnit.CUP_OPEN:
            raise ValueError("L'attributo cup_l deve essere pari a CUP_OPEN o CUP_CLOSE")
        if type(self.cup_f) is not int:
            raise TypeError("L'attributo cup_f deve essere un numero intero")
        if self.cup_f is not ControlUnit.CUP_CLOSE and self.cup_f is not ControlUnit.CUP_OPEN:
            raise ValueError("L'attributo cup_f deve essere pari a CUP_OPEN o CUP_CLOSE")
        if type(self.engine) is not int:
            raise TypeError("L'attributo engine deve essere un numero intero")
        if self.engine is not ControlUnit.ENGINE_OFF and self.engine is not ControlUnit.ENGINE_ON:
            raise ValueError("L'attributo engine deve essere pari a ENGINE_OFF o ENGINE_ON")
        if type(self.alarm) is not int:
            raise TypeError("L'attributo engine deve essere un numero intero")
        if self.alarm is not ControlUnit.ALARM_UNARMED and self.alarm is not ControlUnit.ALARM_ARMED:
            raise ValueError("L'attributo engine deve essere pari a ALARM_UNARMED o ALARM_ARMED")
        if type(self.cup_lock) is not int:
            raise TypeError("L'attributo engine deve essere un numero intero")
        if self.cup_lock is not ControlUnit.CAPS_UNLOCKED and self.cup_lock is not ControlUnit.CAPS_LOCKED:
            raise ValueError("L'attributo engine deve essere pari a CAPS_UNLOCKED o CAPS_LOCKED")
        if type(self.distance_travelled) is not float and type(self.distance_travelled) is not int:
            raise TypeError("L'attributo input_gasoline_f deve essere un numero intero o decimale")
        if not 0 <= self.distance_travelled <= 9999.9:
            raise ValueError(
                "L'attributo distance_travelled deve essere un numero intero o decimale positivo minore di 9999.9"
            )

        return True
