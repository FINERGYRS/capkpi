# Copyright (c) 2022, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import finergy
from finergy.tests.utils import FinergyTestCase

from capkpi.setup.doctype.naming_series.naming_series import NamingSeries


class TestNamingSeries(FinergyTestCase):
	def setUp(self):
		self.ns: NamingSeries = finergy.get_doc("Naming Series")

	def tearDown(self):
		finergy.db.rollback()

	def test_naming_preview(self):
		self.ns.select_doc_for_series = "Sales Invoice"

		self.ns.naming_series_to_check = "AXBZ.####"
		serieses = self.ns.preview_series().split("\n")
		self.assertEqual(["AXBZ0001", "AXBZ0002", "AXBZ0003"], serieses)

		self.ns.naming_series_to_check = "AXBZ-.{currency}.-"
		serieses = self.ns.preview_series().split("\n")

	def test_get_transactions(self):

		naming_info = self.ns.get_transactions()
		self.assertIn("Sales Invoice", naming_info["transactions"])

		existing_naming_series = finergy.get_meta("Sales Invoice").get_field("naming_series").options

		for series in existing_naming_series.split("\n"):
			self.assertIn(series, naming_info["prefixes"])
