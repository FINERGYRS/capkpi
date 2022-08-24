# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy


class TestCashFlowMapping(unittest.TestCase):
	def setUp(self):
		if finergy.db.exists("Cash Flow Mapping", "Test Mapping"):
			finergy.delete_doc("Cash Flow Mappping", "Test Mapping")

	def tearDown(self):
		finergy.delete_doc("Cash Flow Mapping", "Test Mapping")

	def test_multiple_selections_not_allowed(self):
		doc = finergy.new_doc("Cash Flow Mapping")
		doc.mapping_name = "Test Mapping"
		doc.label = "Test label"
		doc.append("accounts", {"account": "Accounts Receivable - _TC"})
		doc.is_working_capital = 1
		doc.is_finance_cost = 1

		self.assertRaises(finergy.ValidationError, doc.insert)

		doc.is_finance_cost = 0
		doc.insert()