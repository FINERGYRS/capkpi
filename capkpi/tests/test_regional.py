import unittest

import finergy

import capkpi


@capkpi.allow_regional
def test_method():
	return "original"


class TestInit(unittest.TestCase):
	def test_regional_overrides(self):
		finergy.flags.country = "Maldives"
		self.assertEqual(test_method(), "original")

		finergy.flags.country = "France"
		self.assertEqual(test_method(), "overridden")
