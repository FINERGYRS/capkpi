# Copyright (c) 2017, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy

test_dependencies = ["Fertilizer"]


class TestCrop(unittest.TestCase):
	def test_crop_period(self):
		basil = finergy.get_doc("Crop", "Basil from seed")
		self.assertEqual(basil.period, 15)
