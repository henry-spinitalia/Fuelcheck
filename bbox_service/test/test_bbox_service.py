from twisted.trial import unittest

class BBoxServiceTestCase():

	def test_add(self):
		calc = Calculation()
        result = calc.add(3, 8)
        self.assertEqual(result, 11)