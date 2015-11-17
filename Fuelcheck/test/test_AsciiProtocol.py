from Fuelcheck.AsciiProtocol import AsciiProtocol
#from twisted.trial import unittest
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
		self.assertEqual(aproto.output_packet, "A57901351535057252702112107201511141152091141416602N012359949E"
											   "011220013002400325842650026003700488880101UUUU00UUUUUU03651")

	def test_decode(self):
		aproto = AsciiProtocol()
		result = aproto.decode("A57901351535057252702112107201511141152091141416602N012359949E0112200130024003258"
								"42650026003700488880101UUUU00UUUUUU03651")
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