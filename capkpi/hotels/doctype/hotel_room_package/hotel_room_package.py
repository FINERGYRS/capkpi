# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class HotelRoomPackage(Document):
	def validate(self):
		if not self.item:
			item = finergy.get_doc(
				dict(
					doctype="Item", item_code=self.name, item_group="Products", is_stock_item=0, stock_uom="Unit"
				)
			)
			item.insert()
			self.item = item.name
