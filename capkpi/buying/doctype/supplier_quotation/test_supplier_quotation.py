# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.tests.utils import FinergyTestCase


class TestPurchaseOrder(FinergyTestCase):
	def test_make_purchase_order(self):
		from capkpi.buying.doctype.supplier_quotation.supplier_quotation import make_purchase_order

		sq = finergy.copy_doc(test_records[0]).insert()

		self.assertRaises(finergy.ValidationError, make_purchase_order, sq.name)

		sq = finergy.get_doc("Supplier Quotation", sq.name)
		sq.submit()
		po = make_purchase_order(sq.name)

		self.assertEqual(po.doctype, "Purchase Order")
		self.assertEqual(len(po.get("items")), len(sq.get("items")))

		po.naming_series = "_T-Purchase Order-"

		for doc in po.get("items"):
			if doc.get("item_code"):
				doc.set("schedule_date", "2013-04-12")

		po.insert()


test_records = finergy.get_test_records("Supplier Quotation")
