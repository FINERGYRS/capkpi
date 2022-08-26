# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors and Contributors
# See license.txt


import finergy

test_records = finergy.get_test_records("Item Attribute")

from finergy.tests.utils import FinergyTestCase

from capkpi.stock.doctype.item_attribute.item_attribute import ItemAttributeIncrementError


class TestItemAttribute(FinergyTestCase):
	def setUp(self):
		super().setUp()
		if finergy.db.exists("Item Attribute", "_Test_Length"):
			finergy.delete_doc("Item Attribute", "_Test_Length")

	def test_numeric_item_attribute(self):
		item_attribute = finergy.get_doc(
			{
				"doctype": "Item Attribute",
				"attribute_name": "_Test_Length",
				"numeric_values": 1,
				"from_range": 0.0,
				"to_range": 100.0,
				"increment": 0,
			}
		)

		self.assertRaises(ItemAttributeIncrementError, item_attribute.save)

		item_attribute.increment = 0.5
		item_attribute.save()
