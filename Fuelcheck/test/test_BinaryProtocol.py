# -*- coding: utf-8 -*-

from Fuelcheck.BinaryProtocol import BinaryProtocol
import unittest
import binascii


class TestBinaryProtocol(unittest.TestCase):

    def test_encode(self):

        bproto = BinaryProtocol()

        bproto.imei = "351535057252702"
        bproto.driver = 1121
        bproto.event = 7
        bproto.unixtime = 1447501929
        bproto.sat = 11
        bproto.lat = 41.694336
        bproto.lon = 12.599915
        bproto.speed = 11.2
        bproto.gasoline_r = 200.1
        bproto.gasoline_l = 300.2
        bproto.gasoline_f = 400.3
        bproto.vin = 25.8
        bproto.vbatt = 4.26
        bproto.input_gasoline_r = 500.2
        bproto.input_gasoline_l = 600.3
        bproto.input_gasoline_f = 700.4
        bproto.input_gasoline_tot = 8888
        bproto.cup_r = BinaryProtocol.CUP_CLOSE
        bproto.cup_l = BinaryProtocol.CUP_OPEN
        bproto.cup_f = BinaryProtocol.CUP_CLOSE
        bproto.engine = BinaryProtocol.ENGINE_ON
        bproto.alarm = BinaryProtocol.ALARM_UNARMED
        bproto.cup_lock = BinaryProtocol.CAPS_UNLOCKED
        bproto.distance_travelled = 365.1

        result = bproto.encode()

        self.assertEqual(result, True)
        self.assertEqual(
            bproto.output_packet,
            binascii.unhexlify(
                '300251898CC5DECD610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8225000430E'
            )
        )

    def test_decode(self):

        bproto = BinaryProtocol()

        # Controllo la lunghezza errata
        with self.assertRaises(ValueError):
            bproto.decode(
                binascii.unhexlify(
                    '300251898CC5DECD610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8225000430EAA'
                )
            )

        with self.assertRaises(ValueError):
            bproto.decode(
                binascii.unhexlify(
                    '200251898CC5DECD610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8225000430E'
                )
            )

        # Ora controllo la traduzione
        result = bproto.decode(
            binascii.unhexlify(
                '300251898CC5DECD610407692047560B00C72642409949417000D107BA0BA30F0201AA018A1373175C1BB8225000430E'
            )
        )

        self.assertEqual(bproto.imei, "351535057252702")
        self.assertEqual(bproto.driver, 1121)
        self.assertEqual(bproto.event, 7)
        self.assertEqual(bproto.unixtime, 1447501929)
        self.assertEqual(bproto.sat, 11)
        self.assertAlmostEqual(bproto.lat, 41.694336, 6)
        self.assertAlmostEqual(bproto.lon, 12.599915, 6)
        self.assertEqual(bproto.speed, 11.2)
        self.assertEqual(bproto.gasoline_r, 200.1)
        self.assertEqual(bproto.gasoline_l, 300.2)
        self.assertEqual(bproto.gasoline_f, 400.3)
        self.assertEqual(bproto.vin, 25.8)
        self.assertEqual(bproto.vbatt, 4.26)
        self.assertEqual(bproto.input_gasoline_r, 500.2)
        self.assertEqual(bproto.input_gasoline_l, 600.3)
        self.assertEqual(bproto.input_gasoline_f, 700.4)
        self.assertEqual(bproto.input_gasoline_tot, 8888)
        self.assertEqual(bproto.cup_r, BinaryProtocol.CUP_CLOSE)
        self.assertEqual(bproto.cup_l, BinaryProtocol.CUP_OPEN)
        self.assertEqual(bproto.cup_f, BinaryProtocol.CUP_CLOSE)
        self.assertEqual(bproto.engine, BinaryProtocol.ENGINE_ON)
        self.assertEqual(bproto.alarm, BinaryProtocol.ALARM_UNARMED)
        self.assertEqual(bproto.cup_lock, BinaryProtocol.CAPS_UNLOCKED)
        self.assertEqual(bproto.distance_travelled, 365.1)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
