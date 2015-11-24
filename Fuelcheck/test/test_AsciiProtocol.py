# -*- coding: utf-8 -*-

from Fuelcheck.AsciiProtocol import AsciiProtocol
# from twisted.trial import unittest
import unittest


class TestAsciiProtocol(unittest.TestCase):

    def test_encode(self):

        aproto = AsciiProtocol()

        aproto.imei = "351535057252702"
        aproto.driver = 1121
        aproto.event = 7
        aproto.unixtime = 1447501929
        aproto.sat = 11
        aproto.lat = 41.694336
        aproto.lon = 12.599915
        aproto.speed = 11.2
        aproto.gasoline_r = 200.1
        aproto.gasoline_l = 300.2
        aproto.gasoline_f = 400.3
        aproto.vin = 25.8
        aproto.vbatt = 4.26
        aproto.input_gasoline_r = 500.2
        aproto.input_gasoline_l = 600.3
        aproto.input_gasoline_f = 700.4
        aproto.input_gasoline_tot = 8888
        aproto.cup_r = AsciiProtocol.CUP_CLOSE
        aproto.cup_l = AsciiProtocol.CUP_OPEN
        aproto.cup_f = AsciiProtocol.CUP_CLOSE
        aproto.engine = AsciiProtocol.ENGINE_ON
        aproto.alarm = AsciiProtocol.ALARM_UNARMED
        aproto.cup_lock = AsciiProtocol.CAPS_UNLOCKED
        aproto.distance_travelled = 365.1

        result = aproto.encode()

        self.assertEqual(result, True)
        self.assertEqual(
            aproto.output_packet,
            "A57901351535057252702112107201511141152091141416602N012359949E011220013002400325842650026003700488880101"
            "UUUU00UUUUUU03651"
        )

    def test_decode(self):

        aproto = AsciiProtocol()
        packet = "A57901351535057252702112107201511141152091141416602N012359949E01122001300240032584265002600370048888"
        packet += "0101UUUU00UUUUUU03651"

        # Test del controllo del campo HDR, diverso da A5
        with self.assertRaises(ValueError):
            aproto.decode("B5" + packet[2:])

        with self.assertRaises(ValueError):
            aproto.decode(packet[0:2] + "89" + packet[4:])  # Test del controllo del campo LEN, diverso da len(str)
            aproto.decode(packet[0:4] + "02" + packet[6:])  # Test del controllo del campo VER, diverso da 1
            aproto.decode(packet[0:6] + "351A35057252702" + packet[21:])  # Test del controllo del campo IMEI, HEX
            aproto.decode(packet[0:6] + "3515a5057252702" + packet[21:])  # Test del controllo del campo IMEI, hex
            aproto.decode(packet[0:6] + "35153s057252702" + packet[21:])  # Test del controllo del campo IMEI, string
            aproto.decode(packet[0:21] + "A121" + packet[25:])  # Test del controllo del campo DRVN, HEX
            aproto.decode(packet[0:21] + "1a21" + packet[25:])  # Test del controllo del campo DRVN, hex
            aproto.decode(packet[0:21] + "11s1" + packet[25:])  # Test del controllo del campo DRVN, string
            aproto.decode(packet[0:25] + "0a" + packet[27:])  # Test del controllo del campo EVTN, HEX
            aproto.decode(packet[0:25] + "0A" + packet[27:])  # Test del controllo del campo EVTN, hex
            aproto.decode(packet[0:25] + "s1" + packet[27:])  # Test del controllo del campo EVTN, string
            aproto.decode(packet[0:27] + "20151314" + packet[35:])  # Test del controllo del campo DATE, wrong
            aproto.decode(packet[0:27] + "201511s4" + packet[35:])  # Test del controllo del campo DATE, string
            aproto.decode(packet[0:35] + "117209" + packet[41:])  # Test del controllo del campo TIME, wrong
            aproto.decode(packet[0:35] + "115t09" + packet[41:])  # Test del controllo del campo TIME, wrong
            aproto.decode(packet[0:41] + "1A" + packet[43:])  # Test del controllo del campo GSAT, string
            aproto.decode(packet[0:43] + "41416602E" + packet[52:])  # Test del controllo del campo LAT, wrong
            aproto.decode(packet[0:43] + "4s416602N" + packet[52:])  # Test del controllo del campo LAT, string
            aproto.decode(packet[0:52] + "012759949N" + packet[62:])  # Test del controllo del campo LONG, wrong
            aproto.decode(packet[0:52] + "012k59949E" + packet[62:])  # Test del controllo del campo LONG, string
            aproto.decode(packet[0:52] + "012k59949E" + packet[62:])  # Test del controllo del campo LONG, string
            aproto.decode(packet[0:62] + "0A12" + packet[66:])  # Test del controllo del campo SPD, HEX
            aproto.decode(packet[0:62] + "01a2" + packet[66:])  # Test del controllo del campo SPD, hex
            aproto.decode(packet[0:62] + "011s" + packet[66:])  # Test del controllo del campo SPD, string
            aproto.decode(packet[0:66] + "A001" + packet[70:])  # Test del controllo del campo FTR, HEX
            aproto.decode(packet[0:66] + "2a01" + packet[70:])  # Test del controllo del campo FTR, hex
            aproto.decode(packet[0:66] + "20h1" + packet[70:])  # Test del controllo del campo FTR, string
            aproto.decode(packet[0:70] + "A002" + packet[74:])  # Test del controllo del campo FTL, HEX
            aproto.decode(packet[0:70] + "3a02" + packet[74:])  # Test del controllo del campo FTL, hex
            aproto.decode(packet[0:70] + "30h2" + packet[74:])  # Test del controllo del campo FTL, string
            aproto.decode(packet[0:74] + "A003" + packet[78:])  # Test del controllo del campo FTF, HEX
            aproto.decode(packet[0:74] + "4a03" + packet[78:])  # Test del controllo del campo FTF, hex
            aproto.decode(packet[0:74] + "40h3" + packet[78:])  # Test del controllo del campo FTF, string
            aproto.decode(packet[0:78] + "A58" + packet[81:])  # Test del controllo del campo MBAT, HEX
            aproto.decode(packet[0:78] + "2a8" + packet[81:])  # Test del controllo del campo MBAT, hex
            aproto.decode(packet[0:78] + "25n" + packet[81:])  # Test del controllo del campo MBAT, string
            aproto.decode(packet[0:81] + "A58" + packet[84:])  # Test del controllo del campo BBAT, HEX
            aproto.decode(packet[0:81] + "2a8" + packet[84:])  # Test del controllo del campo BBAT, hex
            aproto.decode(packet[0:81] + "25n" + packet[84:])  # Test del controllo del campo BBAT, string
            aproto.decode(packet[0:84] + "B002" + packet[88:])  # Test del controllo del campo FCRM, HEX
            aproto.decode(packet[0:84] + "5b02" + packet[88:])  # Test del controllo del campo FCRM, hex
            aproto.decode(packet[0:84] + "50m2" + packet[88:])  # Test del controllo del campo FCRM, string
            aproto.decode(packet[0:88] + "C003" + packet[92:])  # Test del controllo del campo FCLM, HEX
            aproto.decode(packet[0:88] + "6c03" + packet[92:])  # Test del controllo del campo FCLM, hex
            aproto.decode(packet[0:88] + "60l3" + packet[92:])  # Test del controllo del campo FCLM, string
            aproto.decode(packet[0:92] + "C003" + packet[96:])  # Test del controllo del campo FCFM, HEX
            aproto.decode(packet[0:92] + "6c03" + packet[96:])  # Test del controllo del campo FCFM, hex
            aproto.decode(packet[0:92] + "60l3" + packet[96:])  # Test del controllo del campo FCFM, string
            aproto.decode(packet[0:96] + "D888" + packet[100:])  # Test del controllo del campo FCDL, HEX
            aproto.decode(packet[0:96] + "8d88" + packet[100:])  # Test del controllo del campo FCDL, hex
            aproto.decode(packet[0:96] + "88u8" + packet[100:])  # Test del controllo del campo FCDL, string
            aproto.decode(packet[0:100] + "a" + packet[101:])  # Test del controllo del campo FCRS, string
            aproto.decode(packet[0:101] + "a" + packet[102:])  # Test del controllo del campo FCLS, string
            aproto.decode(packet[0:102] + "a" + packet[103:])  # Test del controllo del campo FCFS, string
            aproto.decode(packet[0:103] + "a" + packet[104:])  # Test del controllo del campo IGSS, string
            aproto.decode(packet[0:104] + "a" + packet[105:])  # Test del controllo del campo UNI5, string
            aproto.decode(packet[0:105] + "a" + packet[106:])  # Test del controllo del campo UNI6, string
            aproto.decode(packet[0:106] + "a" + packet[107:])  # Test del controllo del campo UNI7, string
            aproto.decode(packet[0:107] + "a" + packet[108:])  # Test del controllo del campo UNI8, string
            aproto.decode(packet[0:108] + "a" + packet[109:])  # Test del controllo del campo ALRM, string
            aproto.decode(packet[0:109] + "a" + packet[110:])  # Test del controllo del campo FCRL, string
            aproto.decode(packet[0:110] + "a" + packet[111:])  # Test del controllo del campo UNO3, string
            aproto.decode(packet[0:111] + "a" + packet[112:])  # Test del controllo del campo UNO4, string
            aproto.decode(packet[0:112] + "a" + packet[113:])  # Test del controllo del campo UNO5, string
            aproto.decode(packet[0:113] + "a" + packet[114:])  # Test del controllo del campo UNO6, string
            aproto.decode(packet[0:114] + "a" + packet[115:])  # Test del controllo del campo UNO7, string
            aproto.decode(packet[0:115] + "a" + packet[116:])  # Test del controllo del campo UNO8, string
            aproto.decode(packet[0:116] + "A3651")  # Test del controllo del campo HSZZ, HEX
            aproto.decode(packet[0:116] + "0a651")  # Test del controllo del campo HSZZ, hex
            aproto.decode(packet[0:116] + "03s51")  # Test del controllo del campo HSZZ, HEX

        # Ora provo la conversione di tutti i parametri corretti
        result = aproto.decode(self.packet)

        self.assertEqual(result, True)
        self.assertEqual(aproto.header, "A5")
        self.assertEqual(aproto.len, 121)
        self.assertEqual(aproto.version, 1)
        self.assertEqual(aproto.imei, "351535057252702")
        self.assertEqual(aproto.driver, 1121)
        self.assertEqual(aproto.event, 7)
        self.assertEqual(aproto.date_day, 14)
        self.assertEqual(aproto.date_month, 11)
        self.assertEqual(aproto.date_year, 2015)
        self.assertEqual(aproto.time_hour, 11)
        self.assertEqual(aproto.time_minute, 52)
        self.assertEqual(aproto.time_second, 9)
        self.assertEqual(aproto.sat, 11)
        self.assertEqual(aproto.lat, 41.694336)
        self.assertEqual(aproto.lon, 12.599915)
        self.assertEqual(aproto.speed, 11.2)
        self.assertEqual(aproto.gasoline_r, 200.1)
        self.assertEqual(aproto.gasoline_l, 300.2)
        self.assertEqual(aproto.gasoline_f, 400.3)
        self.assertEqual(aproto.vin, 25.8)
        self.assertEqual(aproto.vbatt, 4.26)
        self.assertEqual(aproto.input_gasoline_r, 500.2)
        self.assertEqual(aproto.input_gasoline_l, 600.3)
        self.assertEqual(aproto.input_gasoline_f, 700.4)
        self.assertEqual(aproto.input_gasoline_tot, 8888)
        self.assertEqual(aproto.cup_r, AsciiProtocol.CUP_CLOSE)
        self.assertEqual(aproto.cup_l, AsciiProtocol.CUP_OPEN)
        self.assertEqual(aproto.cup_f, AsciiProtocol.CUP_CLOSE)
        self.assertEqual(aproto.engine, AsciiProtocol.ENGINE_ON)
        self.assertEqual(aproto.unused_inputs, "UUUU")
        self.assertEqual(aproto.alarm, AsciiProtocol.ALARM_UNARMED)
        self.assertEqual(aproto.cup_lock, AsciiProtocol.CAPS_UNLOCKED)
        self.assertEqual(aproto.unused_outputs, "UUUUUU")
        self.assertEqual(aproto.distance_travelled, 365.1)


if __name__ == '__main__':
    unittest.main()
