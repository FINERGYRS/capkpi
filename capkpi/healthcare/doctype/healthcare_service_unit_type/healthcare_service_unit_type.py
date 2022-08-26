# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.model.rename_doc import rename_doc


class HealthcareServiceUnitType(Document):
	def validate(self):
		if self.allow_appointments and self.inpatient_occupancy:
			finergy.msgprint(
				_("Healthcare Service Unit Type cannot have both {0} and {1}").format(
					finergy.bold("Allow Appointments"), finergy.bold("Inpatient Occupancy")
				),
				raise_exception=1,
				title=_("Validation Error"),
				indicator="red",
			)
		elif not self.allow_appointments and not self.inpatient_occupancy:
			finergy.msgprint(
				_("Healthcare Service Unit Type must allow atleast one among {0} and {1}").format(
					finergy.bold("Allow Appointments"), finergy.bold("Inpatient Occupancy")
				),
				raise_exception=1,
				title=_("Validation Error"),
				indicator="red",
			)

		if not self.allow_appointments:
			self.overlap_appointments = 0

		if self.is_billable:
			if self.disabled:
				finergy.db.set_value("Item", self.item, "disabled", 1)
			else:
				finergy.db.set_value("Item", self.item, "disabled", 0)

	def after_insert(self):
		if self.inpatient_occupancy and self.is_billable:
			create_item(self)

	def on_trash(self):
		if self.item:
			try:
				item = self.item
				self.db_set("item", "")
				finergy.delete_doc("Item", item)
			except Exception:
				finergy.throw(_("Not permitted. Please disable the Service Unit Type"))

	def on_update(self):
		if self.change_in_item and self.is_billable and self.item:
			update_item(self)

			item_price = item_price_exists(self)

			if not item_price:
				price_list_name = finergy.db.get_value("Price List", {"selling": 1})
				if self.rate:
					make_item_price(self.item_code, price_list_name, self.rate)
				else:
					make_item_price(self.item_code, price_list_name, 0.0)
			else:
				finergy.db.set_value("Item Price", item_price, "price_list_rate", self.rate)

			finergy.db.set_value(self.doctype, self.name, "change_in_item", 0)
		elif not self.is_billable and self.item:
			finergy.db.set_value("Item", self.item, "disabled", 1)
		self.reload()


def item_price_exists(doc):
	item_price = finergy.db.exists({"doctype": "Item Price", "item_code": doc.item_code})
	if len(item_price):
		return item_price[0][0]
	return False


def create_item(doc):
	# insert item
	item = finergy.get_doc(
		{
			"doctype": "Item",
			"item_code": doc.item_code,
			"item_name": doc.service_unit_type,
			"item_group": doc.item_group,
			"description": doc.description or doc.item_code,
			"is_sales_item": 1,
			"is_service_item": 1,
			"is_purchase_item": 0,
			"is_stock_item": 0,
			"show_in_website": 0,
			"is_pro_applicable": 0,
			"disabled": 0,
			"stock_uom": doc.uom,
		}
	).insert(ignore_permissions=True, ignore_mandatory=True)

	# insert item price
	# get item price list to insert item price
	price_list_name = finergy.db.get_value("Price List", {"selling": 1})
	if doc.rate:
		make_item_price(item.name, price_list_name, doc.rate)
		item.standard_rate = doc.rate
	else:
		make_item_price(item.name, price_list_name, 0.0)
		item.standard_rate = 0.0

	item.save(ignore_permissions=True)

	# Set item in the doc
	doc.db_set("item", item.name)


def make_item_price(item, price_list_name, item_price):
	finergy.get_doc(
		{
			"doctype": "Item Price",
			"price_list": price_list_name,
			"item_code": item,
			"price_list_rate": item_price,
		}
	).insert(ignore_permissions=True, ignore_mandatory=True)


def update_item(doc):
	item = finergy.get_doc("Item", doc.item)
	if item:
		item.update(
			{
				"item_name": doc.service_unit_type,
				"item_group": doc.item_group,
				"disabled": 0,
				"standard_rate": doc.rate,
				"description": doc.description,
			}
		)
		item.db_update()


@finergy.whitelist()
def change_item_code(item, item_code, doc_name):
	if finergy.db.exists({"doctype": "Item", "item_code": item_code}):
		finergy.throw(_("Item with Item Code {0} already exists").format(item_code))
	else:
		rename_doc("Item", item, item_code, ignore_permissions=True)
		finergy.db.set_value("Healthcare Service Unit Type", doc_name, "item_code", item_code)
