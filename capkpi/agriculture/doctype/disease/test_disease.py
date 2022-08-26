# Copyright (c) 2017, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy


class TestDisease(unittest.TestCase):
	def test_treatment_period(self):
		disease = finergy.get_doc("Disease", "Aphids")
		self.assertEqual(disease.treatment_period, 3)
