from finergy.tests.utils import FinergyTestCase

from capkpi.utilities.activation import get_level


class TestActivation(FinergyTestCase):
	def test_activation(self):
		levels = get_level()
		self.assertTrue(levels)
