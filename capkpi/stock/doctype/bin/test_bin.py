# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import finergy
from finergy.tests.utils import FinergyTestCase

from capkpi.stock.doctype.item.test_item import make_item
from capkpi.stock.utils import _create_bin


class TestBin(FinergyTestCase):
	def test_concurrent_inserts(self):
		"""Ensure no duplicates are possible in case of concurrent inserts"""
		item_code = "_TestConcurrentBin"
		make_item(item_code)
		warehouse = "_Test Warehouse - _TC"

		bin1 = finergy.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		bin1.insert()

		bin2 = finergy.get_doc(doctype="Bin", item_code=item_code, warehouse=warehouse)
		with self.assertRaises(finergy.UniqueValidationError):
			bin2.insert()

		# util method should handle it
		bin = _create_bin(item_code, warehouse)
		self.assertEqual(bin.item_code, item_code)

		finergy.db.rollback()

	def test_index_exists(self):
		indexes = finergy.db.sql("show index from tabBin where Non_unique = 0", as_dict=1)
		if not any(index.get("Key_name") == "unique_item_warehouse" for index in indexes):
			self.fail(f"Expected unique index on item-warehouse")
