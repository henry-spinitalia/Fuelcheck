# -*- coding: utf-8 -*-

from Fuelcheck.ControlUnit import ControlUnit
import unittest
import binascii


class TestControlUnit(unittest.TestCase):

    def test_check_values(self):

        ctrl_unit = ControlUnit()

        # Inizializzo le variabili
        ctrl_unit.imei = 351535057252702L
        ctrl_unit.driver = 1121
        ctrl_unit.event = 7
        ctrl_unit.unixtime = 1447501929
        ctrl_unit.sat = 11
        ctrl_unit.lat = 41.694336
        ctrl_unit.lon = 12.599915
        ctrl_unit.speed = 11.2
        ctrl_unit.gasoline_r = 200.1
        ctrl_unit.gasoline_l = 300.2
        ctrl_unit.gasoline_f = 400.3
        ctrl_unit.vin = 25.8
        ctrl_unit.vbatt = 4.26
        ctrl_unit.input_gasoline_r = 500.2
        ctrl_unit.input_gasoline_l = 600.3
        ctrl_unit.input_gasoline_f = 700.4
        ctrl_unit.input_gasoline_tot = 8888
        ctrl_unit.cup_r = ctrl_unit.CUP_CLOSE
        ctrl_unit.cup_l = ctrl_unit.CUP_OPEN
        ctrl_unit.cup_f = ctrl_unit.CUP_CLOSE
        ctrl_unit.engine = ctrl_unit.ENGINE_ON
        ctrl_unit.alarm = ctrl_unit.ALARM_UNARMED
        ctrl_unit.cup_lock = ctrl_unit.CAPS_UNLOCKED
        ctrl_unit.distance_travelled = 365.1
        ctrl_unit.gas_station = 5
        ctrl_unit.text_message = "Come va la trasmissione binaria?"
        ctrl_unit.plate = "AB324LR"

        # Provo a sbagliare lunghezza del campo IMEI, poi lo rendo alfanumerico, poi lo correggo
        ctrl_unit.imei = 35153505725270L
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.imei = 3515350572527021L
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.imei = "351535a57252702"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.imei = 351535057252702L
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Parliamo ora del codice autista
        ctrl_unit.driver = "asd"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.driver = 10000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.driver = 1121
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Vediamo l'evento
        ctrl_unit.event = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.event = 256
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.event = 7
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # La data
        ctrl_unit.unixtime = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.unixtime = 1447501929
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Il numero di satelliti
        ctrl_unit.sat = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.sat = 256
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.sat = 7
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo la latitudine
        ctrl_unit.lat = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.lat = 90.01
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lat = 91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lat = -90.01
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lat = -91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lat = 41.694336
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo la longitudine
        ctrl_unit.lon = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.lon = 181.01
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lon = 182
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lon = -181.01
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lon = -182
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.lon = 12.599915
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo la velocità
        ctrl_unit.speed = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.speed = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.speed = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.speed = 11.2
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo il carburante presente a destra, sinistra, e nel frigo
        ctrl_unit.gasoline_r = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_r = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_r = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_r = 200.1
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.gasoline_l = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_l = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_l = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_l = 300.2
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.gasoline_f = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_f = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_f = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gasoline_f = 400.3
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controlliamo la tensione in ingresso
        ctrl_unit.vin = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.vin = 99.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.vin = 100
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.vin = 25.8
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controlliamo la tensione della batteria interna
        ctrl_unit.vbatt = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.vbatt = 9.991
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.vbatt = 10
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.vbatt = 4.26
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo il carburante presente a destra, sinistra, e nel frigo e totale
        ctrl_unit.input_gasoline_r = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_r = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_r = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_r = 500.2
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.input_gasoline_l = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_l = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_l = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_l = 600.3
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.input_gasoline_f = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_f = 999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_f = 1000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_f = 700.4
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.input_gasoline_tot = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_tot = 10000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.input_gasoline_tot = 8888
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo lo stato dei tappi
        ctrl_unit.cup_r = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.cup_r = 4
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_r = ctrl_unit.CUP_OPEN
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_r = ctrl_unit.CUP_CLOSE
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_r = ctrl_unit.CUP_FAIL
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_r = ctrl_unit.CUP_FAIL
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_l = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.cup_l = 4
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_l = ctrl_unit.CUP_CLOSE
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_l = ctrl_unit.CUP_OPEN
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_l = ctrl_unit.CUP_FAIL
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_l = ctrl_unit.CUP_FAIL
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_f = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.cup_f = 4
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_f = ctrl_unit.CUP_OPEN
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_f = ctrl_unit.CUP_CLOSE
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_f = ctrl_unit.CUP_FAIL
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_f = ctrl_unit.CUP_FAIL
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo lo stato del motore
        ctrl_unit.engine = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.engine = 2
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.engine = ctrl_unit.ENGINE_OFF
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.engine = ctrl_unit.ENGINE_ON
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo lo stato dell'allarme
        ctrl_unit.alarm = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.alarm = 2
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.alarm = ctrl_unit.ALARM_ARMED
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.alarm = ctrl_unit.ALARM_UNARMED
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo lo stato del blocco tappi
        ctrl_unit.cup_lock = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.cup_lock = 2
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_lock = ctrl_unit.CAPS_LOCKED
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_lock = ctrl_unit.CAPS_UNLOCKED
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Controllo la distanza percorsa
        ctrl_unit.distance_travelled = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.distance_travelled = 9999.91
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.distance_travelled = 10000
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.distance_travelled = 365.1
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Vediamo l'ID della stazione di servizio
        ctrl_unit.gas_station = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.gas_station = 100
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gas_station = -1
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.gas_station = 5
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Vediamo il messaggio di test per la chat
        ctrl_unit.text_message = 2.12
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.text_message = 256
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.text_message = 256L
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.text_message = "Questo messaggio di testo può essere arbitrariamente lungo e contenere al massimo" \
                                 " 130 caratteri, ma questa eccede il limite fissato di 14 bytes"
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.text_message = "5"
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.text_message = "Questo messaggio di testo può essere arbitrariamente lungo e contenere al massimo " \
                                 "130 caratteri, e questo non eccede il limite!!!"
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.text_message = ""
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

        # Vediamo la targa
        ctrl_unit.plate = 2.12
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.plate = 256
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.plate = 256L
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.plate = "La targa dovrebbe essere una stringa di max 20 caratteri (vedi ad esempio i rimorchi)"
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.plate = "5"
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.plate = "20 caratteri sono OK"
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.plate = ""
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)

    def test_encode_ascii(self):

        ctrl_unit = ControlUnit()

        ctrl_unit.imei = 351535057252702L
        ctrl_unit.driver = 1121
        ctrl_unit.event = 7
        ctrl_unit.unixtime = 1447501929
        ctrl_unit.sat = 11
        ctrl_unit.lat = 41.694336
        ctrl_unit.lon = 12.599915
        ctrl_unit.speed = 11.2
        ctrl_unit.gasoline_r = 200.1
        ctrl_unit.gasoline_l = 300.2
        ctrl_unit.gasoline_f = 400.3
        ctrl_unit.vin = 25.8
        ctrl_unit.vbatt = 4.26
        ctrl_unit.input_gasoline_r = 500.2
        ctrl_unit.input_gasoline_l = 600.3
        ctrl_unit.input_gasoline_f = 700.4
        ctrl_unit.input_gasoline_tot = 8888
        ctrl_unit.cup_r = ControlUnit.CUP_CLOSE
        ctrl_unit.cup_l = ControlUnit.CUP_OPEN
        ctrl_unit.cup_f = ControlUnit.CUP_FAIL
        ctrl_unit.engine = ControlUnit.ENGINE_ON
        ctrl_unit.alarm = ControlUnit.ALARM_UNARMED
        ctrl_unit.cup_lock = ControlUnit.CAPS_UNLOCKED
        ctrl_unit.distance_travelled = 365.1
        ctrl_unit.gas_station = 5
        ctrl_unit.text_message = "Questo e' un messaggio di testo"
        ctrl_unit.plate = "AB324LR"

        # Evento di base
        result = ctrl_unit.encode_ascii()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            "A57901351535057252702112107201511141152091141416602N012359949E0112200130024003258426500260037004888801F1"
            "UUUU00UUUUUU03651"
        )

        # Rifornimento
        ctrl_unit.event = 13
        result = ctrl_unit.encode_ascii()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            "A57901351535057252702112113201511141152091141416602N012359949E0112200130024003258426500260037004888801F1"
            "UUUU00UUUUUU0365105"
        )

        # Messaggio di testo
        ctrl_unit.event = 14
        result = ctrl_unit.encode_ascii()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            "A57901351535057252702112114201511141152091141416602N012359949E0112200130024003258426500260037004888801F1"
            "UUUU00UUUUUU03651Questo e' un messaggio di testo$"
        )

        # Messaggio di rifornimento da cisterna
        ctrl_unit.event = 15
        result = ctrl_unit.encode_ascii()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            "A57901351535057252702112115201511141152091141416602N012359949E0112200130024003258426500260037004888801F1"
            "UUUU00UUUUUU03651AB324LR$"
        )

    def test_decode_ascii(self):

        ctrl_unit = ControlUnit()

        # Evento di base
        packet = "A57901351535057252702112107201511141152091141416602N012359949E01122001300240032584265002600370048888"
        packet += "0101UUUU00UUUUUU03651"

        # Test del controllo del campo HDR, diverso da A5
        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii("B5" + packet[2:])

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:2] + "89" + packet[4:])  # Test del campo LEN != len(str)

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:4] + "02" + packet[6:])  # Test del campo VER != 1

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:6] + "351A35057252702" + packet[21:])  # Test del campo IMEI, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:6] + "3515a5057252702" + packet[21:])  # Test del campo IMEI, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:6] + "35153s057252702" + packet[21:])  # Test del campo IMEI, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:21] + "A121" + packet[25:])  # Test del campo DRVN, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:21] + "1a21" + packet[25:])  # Test del campo DRVN, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:21] + "11s1" + packet[25:])  # Test del campo DRVN, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:25] + "0a" + packet[27:])  # Test del campo EVTN, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:25] + "s1" + packet[27:])  # Test del campo EVTN, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:27] + "20151314" + packet[35:])  # Test del campo DATE, wrong

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:27] + "201511s4" + packet[35:])  # Test del campo DATE, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:35] + "117209" + packet[41:])  # Test del campo TIME, wrong

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:35] + "115t09" + packet[41:])  # Test del campo TIME, wrong

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:41] + "1A" + packet[43:])  # Test del campo GSAT, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:43] + "41416602E" + packet[52:])  # Test del campo LAT, wrong

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:43] + "4s416602N" + packet[52:])  # Test del campo LAT, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:52] + "012759949N" + packet[62:])  # Test del campo LONG, wrong

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:52] + "012k59949E" + packet[62:])  # Test del campo LONG, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:52] + "012k59949E" + packet[62:])  # Test del campo LONG, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:62] + "0A12" + packet[66:])  # Test del campo SPD, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:62] + "01a2" + packet[66:])  # Test del campo SPD, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:62] + "011s" + packet[66:])  # Test del campo SPD, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:66] + "A001" + packet[70:])  # Test del campo FTR, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:66] + "2a01" + packet[70:])  # Test del campo FTR, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:66] + "20h1" + packet[70:])  # Test del campo FTR, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:70] + "A002" + packet[74:])  # Test del campo FTL, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:70] + "3a02" + packet[74:])  # Test del campo FTL, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:70] + "30h2" + packet[74:])  # Test del campo FTL, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:74] + "A003" + packet[78:])  # Test del campo FTF, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:74] + "4a03" + packet[78:])  # Test del  campo FTF, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:74] + "40h3" + packet[78:])  # Test del campo FTF, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:78] + "A58" + packet[81:])  # Test del campo MBAT, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:78] + "2a8" + packet[81:])  # Test del campo MBAT, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:78] + "25n" + packet[81:])  # Test del campo MBAT, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:81] + "A58" + packet[84:])  # Test del campo BBAT, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:81] + "2a8" + packet[84:])  # Test del campo BBAT, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:81] + "25n" + packet[84:])  # Test del campo BBAT, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:84] + "B002" + packet[88:])  # Test del campo FCRM, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:84] + "5b02" + packet[88:])  # Test del campo FCRM, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:84] + "50m2" + packet[88:])  # Test del campo FCRM, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:88] + "C003" + packet[92:])  # Test del campo FCLM, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:88] + "6c03" + packet[92:])  # Test del campo FCLM, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:88] + "60l3" + packet[92:])  # Test del campo FCLM, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:92] + "C003" + packet[96:])  # Test del campo FCFM, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:92] + "6c03" + packet[96:])  # Test del campo FCFM, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:92] + "60l3" + packet[96:])  # Test del campo FCFM, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:96] + "D888" + packet[100:])  # Test del campo FCDL, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:96] + "8d88" + packet[100:])  # Test del campo FCDL, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:96] + "88u8" + packet[100:])  # Test del campo FCDL, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:100] + "a" + packet[101:])  # Test del campo FCRS, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:101] + "a" + packet[102:])  # Test del campo FCLS, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:102] + "a" + packet[103:])  # Test del campo FCFS, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:103] + "a" + packet[104:])  # Test del campo IGSS, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:108] + "a" + packet[109:])  # Test del campo ALRM, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:109] + "a" + packet[110:])  # Test del campo FCRL, string

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:116] + "A3651")  # Test del campo HSZZ, HEX

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:116] + "0a651")  # Test del campo HSZZ, hex

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:116] + "03s51")  # Test del campo HSZZ, HEX

        # Ora provo la conversione di tutti i parametri corretti
        result = ctrl_unit.decode_ascii(packet)

        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.ascii_header, "A5")
        self.assertEqual(ctrl_unit.imei, 351535057252702L)
        self.assertEqual(ctrl_unit.driver, 1121)
        self.assertEqual(ctrl_unit.event, 7)
        self.assertEqual(ctrl_unit.unixtime, 1447501929)
        self.assertEqual(ctrl_unit.sat, 11)
        self.assertAlmostEqual(ctrl_unit.lat, 41.694337, 6)
        self.assertAlmostEqual(ctrl_unit.lon, 12.599915, 6)
        self.assertEqual(ctrl_unit.speed, 11.2)
        self.assertEqual(ctrl_unit.gasoline_r, 200.1)
        self.assertEqual(ctrl_unit.gasoline_l, 300.2)
        self.assertEqual(ctrl_unit.gasoline_f, 400.3)
        self.assertEqual(ctrl_unit.vin, 25.8)
        self.assertEqual(ctrl_unit.vbatt, 4.26)
        self.assertEqual(ctrl_unit.input_gasoline_r, 500.2)
        self.assertEqual(ctrl_unit.input_gasoline_l, 600.3)
        self.assertEqual(ctrl_unit.input_gasoline_f, 700.4)
        self.assertEqual(ctrl_unit.input_gasoline_tot, 8888)
        self.assertEqual(ctrl_unit.cup_r, ControlUnit.CUP_CLOSE)
        self.assertEqual(ctrl_unit.cup_l, ControlUnit.CUP_OPEN)
        self.assertEqual(ctrl_unit.cup_f, ControlUnit.CUP_CLOSE)
        self.assertEqual(ctrl_unit.engine, ControlUnit.ENGINE_ON)
        self.assertEqual(ctrl_unit.unused_inputs, "UUUU")
        self.assertEqual(ctrl_unit.alarm, ControlUnit.ALARM_UNARMED)
        self.assertEqual(ctrl_unit.cup_lock, ControlUnit.CAPS_UNLOCKED)
        self.assertEqual(ctrl_unit.unused_outputs, "UUUUUU")
        self.assertEqual(ctrl_unit.distance_travelled, 365.1)

        # Rifornimento
        packet = "A57B01351535057252702112113201511141152091141416602N012359949E01122001300240032584265002600370048888"
        packet += "0101UUUU00UUUUUU0365105"

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:121] + "0D")  # Test del campo DIST, NUM

        # Ora provo la conversione di tutti i parametri ed analizzo l'ultimo introdotto
        result = ctrl_unit.decode_ascii(packet)
        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.gas_station, 5)

        # Messaggio di testo
        packet = "A57901351535057252702112114201511141152091141416602N012359949E01122001300240032584265002600370048888"
        packet += "0101UUUU00UUUUUU03651Questo e' un messaggio di testo$"

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:121] + "Questo è un messaggio di testo")  # Test del campo CHAT, STR

        # Ora provo la conversione di tutti i parametri ed analizzo l'ultimo introdotto
        result = ctrl_unit.decode_ascii(packet)
        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.text_message, "Questo e' un messaggio di testo")

        # Messaggio di rifornimento da cisterna
        packet = "A57901351535057252702112115201511141152091141416602N012359949E01122001300240032584265002600370048888"
        packet += "0101UUUU00UUUUUU03651AB123CD$"

        with self.assertRaises(ValueError):
            ctrl_unit.decode_ascii(packet[0:121] + "AB123CD")  # Test del campo TARG, STR

        # Ora provo la conversione di tutti i parametri ed analizzo l'ultimo introdotto
        result = ctrl_unit.decode_ascii(packet)
        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.plate, "AB123CD")

    def test_encode_binary(self):

        ctrl_unit = ControlUnit()

        ctrl_unit.imei = 351535057252702L
        ctrl_unit.driver = 1121
        ctrl_unit.event = 7
        ctrl_unit.unixtime = 1447501929
        ctrl_unit.sat = 11
        ctrl_unit.lat = 41.694336
        ctrl_unit.lon = 12.599915
        ctrl_unit.speed = 11.2
        ctrl_unit.gasoline_r = 200.1
        ctrl_unit.gasoline_l = 300.2
        ctrl_unit.gasoline_f = 400.3
        ctrl_unit.vin = 25.8
        ctrl_unit.vbatt = 4.26
        ctrl_unit.input_gasoline_r = 500.2
        ctrl_unit.input_gasoline_l = 600.3
        ctrl_unit.input_gasoline_f = 700.4
        ctrl_unit.input_gasoline_tot = 8888
        ctrl_unit.cup_r = ControlUnit.CUP_FAIL
        ctrl_unit.cup_l = ControlUnit.CUP_OPEN
        ctrl_unit.cup_f = ControlUnit.CUP_CLOSE
        ctrl_unit.engine = ControlUnit.ENGINE_ON
        ctrl_unit.alarm = ControlUnit.ALARM_UNARMED
        ctrl_unit.cup_lock = ControlUnit.CAPS_UNLOCKED
        ctrl_unit.distance_travelled = 365.1
        ctrl_unit.gas_station = 5
        ctrl_unit.text_message = "Come va la trasmissione binaria?"
        ctrl_unit.plate = "AB324LR"

        # Evento di base
        result = ctrl_unit.encode_binary()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            binascii.unhexlify(
                '32025EB13622B83F0100610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E'
            )
        )

        # Rifornimento
        ctrl_unit.event = 13
        result = ctrl_unit.encode_binary()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            binascii.unhexlify(
                '33025EB13622B83F010061040D692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E05'
            )
        )

        # Messaggio di testo
        ctrl_unit.event = 14
        result = ctrl_unit.encode_binary()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            binascii.unhexlify(
                'B4025EB13622B83F010061040E692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E'
                '436F6D65207661206C6120747261736D697373696F6E652062696E617269613F000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                '000000000000000000000000000000000000000000000000000000000000'
            )
        )

        # Messaggio di rifornimento da cisterna
        ctrl_unit.event = 15
        result = ctrl_unit.encode_binary()

        self.assertEqual(result, True)
        self.assertEqual(
            ctrl_unit.output_packet,
            binascii.unhexlify(
                '46025EB13622B83F010061040F692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E'
                '41423332344C5200000000000000000000000000'
            )
        )

    def test_decode_binary(self):

        ctrl_unit = ControlUnit()

        # Controllo la lunghezza errata
        with self.assertRaises(ValueError):
            ctrl_unit.decode_binary(
                binascii.unhexlify(
                    '300251898CC5DECD610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8225000430EAA'
                )
            )

        with self.assertRaises(ValueError):
            ctrl_unit.decode_binary(
                binascii.unhexlify(
                    '200251898CC5DECD610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8225000430E'
                )
            )

        # Ora controllo la traduzione
        result = ctrl_unit.decode_binary(
            binascii.unhexlify(
                '32025EB13622B83F0100610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E'
            )
        )

        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.imei, 351535057252702L)
        self.assertEqual(ctrl_unit.driver, 1121)
        self.assertEqual(ctrl_unit.event, 7)
        self.assertEqual(ctrl_unit.unixtime, 1447501929)
        self.assertEqual(ctrl_unit.sat, 11)
        self.assertAlmostEqual(ctrl_unit.lat, 41.694336, 6)
        self.assertAlmostEqual(ctrl_unit.lon, 12.599915, 6)
        self.assertEqual(ctrl_unit.speed, 11.2)
        self.assertEqual(ctrl_unit.gasoline_r, 200.1)
        self.assertEqual(ctrl_unit.gasoline_l, 300.2)
        self.assertEqual(ctrl_unit.gasoline_f, 400.3)
        self.assertEqual(ctrl_unit.vin, 25.8)
        self.assertEqual(ctrl_unit.vbatt, 4.26)
        self.assertEqual(ctrl_unit.input_gasoline_r, 500.2)
        self.assertEqual(ctrl_unit.input_gasoline_l, 600.3)
        self.assertEqual(ctrl_unit.input_gasoline_f, 700.4)
        self.assertEqual(ctrl_unit.input_gasoline_tot, 8888)
        self.assertEqual(ctrl_unit.cup_r, ControlUnit.CUP_FAIL)
        self.assertEqual(ctrl_unit.cup_l, ControlUnit.CUP_OPEN)
        self.assertEqual(ctrl_unit.cup_f, ControlUnit.CUP_CLOSE)
        self.assertEqual(ctrl_unit.engine, ControlUnit.ENGINE_ON)
        self.assertEqual(ctrl_unit.alarm, ControlUnit.ALARM_UNARMED)
        self.assertEqual(ctrl_unit.cup_lock, ControlUnit.CAPS_UNLOCKED)
        self.assertEqual(ctrl_unit.distance_travelled, 365.1)

        # Ora controllo la traduzione dell'evento 13
        result = ctrl_unit.decode_binary(
            binascii.unhexlify(
                '33025EB13622B83F010061040D692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E05'
            )
        )

        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.event, 13)
        self.assertEqual(ctrl_unit.gas_station, 5)

        # Ora controllo la traduzione dell'evento 14
        result = ctrl_unit.decode_binary(
            binascii.unhexlify(
                'B4025EB13622B83F010061040E692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E'
                '436F6D65207661206C6120747261736D697373696F6E652062696E617269613F000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                '000000000000000000000000000000000000000000000000000000000000'
            )
        )

        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.event, 14)
        self.assertEqual(ctrl_unit.text_message, "Come va la trasmissione binaria?")

        # Ora controllo la traduzione dell'evento 15
        result = ctrl_unit.decode_binary(
            binascii.unhexlify(
                '46025EB13622B83F010061040F692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8226E00430E'
                '41423332344C5200000000000000000000000000'
            )
        )

        self.assertEqual(result, True)
        self.assertEqual(ctrl_unit.event, 15)
        self.assertEqual(ctrl_unit.plate, "AB324LR")

    def test_direct_loop(self):

        ctrl_unit = ControlUnit()

        input_mex = "A57901351535057249088454500201512011056360000000000N000000000E0000008200920096111419" \
                    "00000000000000000FF1UUUU10UUUUUU00000"

        ctrl_unit.decode_ascii(input_mex)
        ctrl_unit.encode_binary()

        ctrl_unit.decode_binary(ctrl_unit.output_packet)
        ctrl_unit.encode_ascii()

        self.assertEqual(input, ctrl_unit.output_packet)

    def test_deprecation_warning(self):

        ctrl_unit = ControlUnit()

        input_mex = "A57901356496042398040000000201512021722030000000000N000000000E0000002400180034128386" \
                    "00000000000000000101FUUU00UUUUUU00000"

        ctrl_unit.decode_ascii(input_mex)

if __name__ == '__main__':
    unittest.main()