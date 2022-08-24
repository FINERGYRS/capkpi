# Copyright (c) 2022, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import finergy
from finergy.tests.utils import FinergyTestCase

from capkpi.manufacturing.doctype.bom_update_log.test_bom_update_log import (
	update_cost_in_all_boms_in_test,
)
from capkpi.manufacturing.doctype.bom_update_tool.bom_update_tool import enqueue_replace_bom
from capkpi.manufacturing.doctype.production_plan.test_production_plan import make_bom
from capkpi.stock.doctype.item.test_item import create_item

test_records = finergy.get_test_records("BOM")


class TestBOMUpdateTool(FinergyTestCase):
	"Test major functions run via BOM Update Tool."

	def tearDown(self):
		finergy.db.rollback()

	def test_replace_bom(self):
		current_bom = "BOM-_Test Item Home Desktop Manufactured-001"

		bom_doc = finergy.copy_doc(test_records[0])
		bom_doc.items[1].item_code = "_Test Item"
		bom_doc.insert()

		boms = finergy._dict(current_bom=current_bom, new_bom=bom_doc.name)
		enqueue_replace_bom(boms=boms)

		self.assertFalse(finergy.db.exists("BOM Item", {"bom_no": current_bom, "docstatus": 1}))
		self.assertTrue(finergy.db.exists("BOM Item", {"bom_no": bom_doc.name, "docstatus": 1}))

	def test_bom_cost(self):
		for item in ["BOM Cost Test Item 1", "BOM Cost Test Item 2", "BOM Cost Test Item 3"]:
			item_doc = create_item(item, valuation_rate=100)
			if item_doc.valuation_rate != 100.00:
				finergy.db.set_value("Item", item_doc.name, "valuation_rate", 100)

		bom_no = finergy.db.get_value("BOM", {"item": "BOM Cost Test Item 1"}, "name")
		if not bom_no:
			doc = make_bom(
				item="BOM Cost Test Item 1",
				raw_materials=["BOM Cost Test Item 2", "BOM Cost Test Item 3"],
				currency="INR",
			)
		else:
			doc = finergy.get_doc("BOM", bom_no)

		self.assertEqual(doc.total_cost, 200)

		finergy.db.set_value("Item", "BOM Cost Test Item 2", "valuation_rate", 200)
		update_cost_in_all_boms_in_test()

		doc.load_from_db()
		self.assertEqual(doc.total_cost, 300)

		finergy.db.set_value("Item", "BOM Cost Test Item 2", "valuation_rate", 100)
		update_cost_in_all_boms_in_test()

		doc.load_from_db()
		self.assertEqual(doc.total_cost, 200)
