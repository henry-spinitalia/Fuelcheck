from Fuelcheck.BinaryProtocol import BinaryProtocol
import unittest


class TestBinaryProtocol(unittest.TestCase):

	def test_encode(self):
		bproto = BinaryProtocol()
		# self.fail()
		self.assertEqual(True, False)

	def test_decode(self):
		bproto = BinaryProtocol()
		self.assertEqual(True, False)

if __name__ == '__main__':
	unittest.main()
