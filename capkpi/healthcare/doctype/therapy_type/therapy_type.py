# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy import _
from finergy.model.document import Document
from finergy.model.rename_doc import rename_doc
from finergy.utils import cint


class TherapyType(Document):
	def validate(self):
		self.enable_disable_item()

	def after_insert(self):
		create_item_from_therapy(self)

	def on_update(self):
		if self.change_in_item:
			self.update_item_and_item_price()

	def enable_disable_item(self):
		if self.is_billable:
			if self.disabled:
				finergy.db.set_value("Item", self.item, "disabled", 1)
			else:
				finergy.db.set_value("Item", self.item, "disabled", 0)

	def update_item_and_item_price(self):
		if self.is_billable and self.item:
			item_doc = finergy.get_doc("Item", {"item_code": self.item})
			item_doc.item_name = self.item_name
			item_doc.item_group = self.item_group
			item_doc.description = self.description
			item_doc.disabled = 0
			item_doc.ignore_mandatory = True
			item_doc.save(ignore_permissions=True)

			if self.rate:
				item_price = finergy.get_doc("Item Price", {"item_code": self.item})
				item_price.item_name = self.item_name
				item_price.price_list_rate = self.rate
				item_price.ignore_mandatory = True
				item_price.save()

		elif not self.is_billable and self.item:
			finergy.db.set_value("Item", self.item, "disabled", 1)

		self.db_set("change_in_item", 0)

	@finergy.whitelist()
	def add_exercises(self):
		exercises = self.get_exercises_for_body_parts()
		last_idx = max(
			[cint(d.idx) for d in self.get("exercises")]
			or [
				0,
			]
		)
		for i, d in enumerate(exercises):
			ch = self.append("exercises", {})
			ch.exercise_type = d.parent
			ch.idx = last_idx + i + 1

	def get_exercises_for_body_parts(self):
		body_parts = [entry.body_part for entry in self.therapy_for]

		exercises = finergy.db.sql(
			"""
				SELECT DISTINCT
					b.parent, e.name, e.difficulty_level
				FROM
				 	`tabExercise Type` e, `tabBody Part Link` b
				WHERE
					b.body_part IN %(body_parts)s AND b.parent=e.name
			""",
			{"body_parts": body_parts},
			as_dict=1,
		)

		return exercises


def create_item_from_therapy(doc):
	disabled = doc.disabled
	if doc.is_billable and not doc.disabled:
		disabled = 0

	uom = finergy.db.exists("UOM", "Unit") or finergy.db.get_single_value("Stock Settings", "stock_uom")

	item = finergy.get_doc(
		{
			"doctype": "Item",
			"item_code": doc.item_code,
			"item_name": doc.item_name,
			"item_group": doc.item_group,
			"description": doc.description,
			"is_sales_item": 1,
			"is_service_item": 1,
			"is_purchase_item": 0,
			"is_stock_item": 0,
			"show_in_website": 0,
			"is_pro_applicable": 0,
			"disabled": disabled,
			"stock_uom": uom,
		}
	).insert(ignore_permissions=True, ignore_mandatory=True)

	make_item_price(item.name, doc.rate)
	doc.db_set("item", item.name)


def make_item_price(item, item_price):
	price_list_name = finergy.db.get_value("Price List", {"selling": 1})
	finergy.get_doc(
		{
			"doctype": "Item Price",
			"price_list": price_list_name,
			"item_code": item,
			"price_list_rate": item_price,
		}
	).insert(ignore_permissions=True, ignore_mandatory=True)


@finergy.whitelist()
def change_item_code_from_therapy(item_code, doc):
	doc = finergy._dict(json.loads(doc))

	if finergy.db.exists("Item", {"item_code": item_code}):
		finergy.throw(_("Item with Item Code {0} already exists").format(item_code))
	else:
		rename_doc("Item", doc.item, item_code, ignore_permissions=True)
		finergy.db.set_value("Therapy Type", doc.name, "item_code", item_code)
	return
