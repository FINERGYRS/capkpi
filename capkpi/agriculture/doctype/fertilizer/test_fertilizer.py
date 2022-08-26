# Copyright (c) 2017, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy


class TestFertilizer(unittest.TestCase):
	def test_fertilizer_creation(self):
		self.assertEqual(finergy.db.exists("Fertilizer", "Urea"), "Urea")
