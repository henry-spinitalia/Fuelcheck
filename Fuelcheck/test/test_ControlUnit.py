# -*- coding: utf-8 -*-

from Fuelcheck.ControlUnit import ControlUnit
import unittest


class TestControlUnit(unittest.TestCase):

    def test_check_values(self):

        ctrl_unit = ControlUnit()

        # Inizializzo le variabili
        ctrl_unit.imei = "351535057252702"
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

        # Provo a sbagliare lunghezza del campo IMEI, poi lo rendo alfanumerico, poi lo correggo
        ctrl_unit.imei = "35153505725270"
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.imei = "3515350572527021"
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.imei = "351535a57252702"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.imei = "351535057252702"
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
        ctrl_unit.cup_r = 2
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_r = ctrl_unit.CUP_OPEN
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_r = ctrl_unit.CUP_CLOSE
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_l = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.cup_l = 2
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_l = ctrl_unit.CUP_CLOSE
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_l = ctrl_unit.CUP_OPEN
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_f = "a"
        with self.assertRaises(TypeError):
            ctrl_unit.check_values()
        ctrl_unit.cup_f = 2
        with self.assertRaises(ValueError):
            ctrl_unit.check_values()
        ctrl_unit.cup_f = ctrl_unit.CUP_OPEN
        result = ctrl_unit.check_values()
        self.assertEqual(result, True)
        ctrl_unit.cup_f = ctrl_unit.CUP_CLOSE
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


if __name__ == '__main__':
    unittest.main()