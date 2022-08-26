# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy import _
from finergy.model.document import Document

from capkpi.controllers.queries import item_query


class RestaurantOrderEntry(Document):
	pass


@finergy.whitelist()
def get_invoice(table):
	"""returns the active invoice linked to the given table"""
	invoice_name = finergy.get_value("Sales Invoice", dict(restaurant_table=table, docstatus=0))
	restaurant, menu_name = get_restaurant_and_menu_name(table)
	if invoice_name:
		invoice = finergy.get_doc("Sales Invoice", invoice_name)
	else:
		invoice = finergy.new_doc("Sales Invoice")
		invoice.naming_series = finergy.db.get_value("Restaurant", restaurant, "invoice_series_prefix")
		invoice.is_pos = 1
		default_customer = finergy.db.get_value("Restaurant", restaurant, "default_customer")
		if not default_customer:
			finergy.throw(_("Please set default customer in Restaurant Settings"))
		invoice.customer = default_customer

	invoice.taxes_and_charges = finergy.db.get_value("Restaurant", restaurant, "default_tax_template")
	invoice.selling_price_list = finergy.db.get_value(
		"Price List", dict(restaurant_menu=menu_name, enabled=1)
	)

	return invoice


@finergy.whitelist()
def sync(table, items):
	"""Sync the sales order related to the table"""
	invoice = get_invoice(table)
	items = json.loads(items)

	invoice.items = []
	invoice.restaurant_table = table
	for d in items:
		invoice.append("items", dict(item_code=d.get("item"), qty=d.get("qty")))

	invoice.save()
	return invoice.as_dict()


@finergy.whitelist()
def make_invoice(table, customer, mode_of_payment):
	"""Make table based on Sales Order"""
	restaurant, menu = get_restaurant_and_menu_name(table)
	invoice = get_invoice(table)
	invoice.customer = customer
	invoice.restaurant = restaurant
	invoice.calculate_taxes_and_totals()
	invoice.append("payments", dict(mode_of_payment=mode_of_payment, amount=invoice.grand_total))
	invoice.save()
	invoice.submit()

	finergy.msgprint(_("Invoice Created"), indicator="green", alert=True)

	return invoice.name


@finergy.whitelist()
def item_query_restaurant(
	doctype="Item", txt="", searchfield="name", start=0, page_len=20, filters=None, as_dict=False
):
	"""Return items that are selected in active menu of the restaurant"""
	restaurant, menu = get_restaurant_and_menu_name(filters["table"])
	items = finergy.db.get_all("Restaurant Menu Item", ["item"], dict(parent=menu))
	del filters["table"]
	filters["name"] = ("in", [d.item for d in items])

	return item_query("Item", txt, searchfield, start, page_len, filters, as_dict)


def get_restaurant_and_menu_name(table):
	if not table:
		finergy.throw(_("Please select a table"))

	restaurant = finergy.db.get_value("Restaurant Table", table, "restaurant")
	menu = finergy.db.get_value("Restaurant", restaurant, "active_menu")

	if not menu:
		finergy.throw(_("Please set an active menu for Restaurant {0}").format(restaurant))

	return restaurant, menu
