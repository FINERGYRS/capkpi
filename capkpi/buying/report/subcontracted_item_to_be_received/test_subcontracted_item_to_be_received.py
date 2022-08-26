# Python bytecode 2.7 (62211)
# Embedded file name: /Users/anuragmishra/finergy-develop/apps/capkpi/capkpi/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py
# Compiled at: 2019-05-06 09:51:46
# Decompiled by https://python-decompiler.com


import finergy
from finergy.tests.utils import FinergyTestCase

from capkpi.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
from capkpi.buying.doctype.purchase_order.test_purchase_order import create_purchase_order
from capkpi.buying.report.subcontracted_item_to_be_received.subcontracted_item_to_be_received import (
	execute,
)
from capkpi.stock.doctype.stock_entry.test_stock_entry import make_stock_entry


class TestSubcontractedItemToBeReceived(FinergyTestCase):
	def test_pending_and_received_qty(self):
		po = create_purchase_order(item_code="_Test FG Item", is_subcontracted="Yes")
		transfer_param = []
		make_stock_entry(
			item_code="_Test Item", target="_Test Warehouse 1 - _TC", qty=100, basic_rate=100
		)
		make_stock_entry(
			item_code="_Test Item Home Desktop 100",
			target="_Test Warehouse 1 - _TC",
			qty=100,
			basic_rate=100,
		)
		make_purchase_receipt_against_po(po.name)
		po.reload()
		col, data = execute(
			filters=finergy._dict(
				{
					"supplier": po.supplier,
					"from_date": finergy.utils.get_datetime(
						finergy.utils.add_to_date(po.transaction_date, days=-10)
					),
					"to_date": finergy.utils.get_datetime(finergy.utils.add_to_date(po.transaction_date, days=10)),
				}
			)
		)
		self.assertEqual(data[0]["pending_qty"], 5)
		self.assertEqual(data[0]["received_qty"], 5)
		self.assertEqual(data[0]["purchase_order"], po.name)
		self.assertEqual(data[0]["supplier"], po.supplier)


def make_purchase_receipt_against_po(po, quantity=5):
	pr = make_purchase_receipt(po)
	pr.items[0].qty = quantity
	pr.supplier_warehouse = "_Test Warehouse 1 - _TC"
	pr.insert()
	pr.submit()
