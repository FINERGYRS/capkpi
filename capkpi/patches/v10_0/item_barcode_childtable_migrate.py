# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("stock", "doctype", "item_barcode")
	if finergy.get_all("Item Barcode", limit=1):
		return
	if "barcode" not in finergy.db.get_table_columns("Item"):
		return

	items_barcode = finergy.db.sql(
		"select name, barcode from tabItem where barcode is not null", as_dict=True
	)
	finergy.reload_doc("stock", "doctype", "item")

	for item in items_barcode:
		barcode = item.barcode.strip()

		if barcode and "<" not in barcode:
			try:
				finergy.get_doc(
					{
						"idx": 0,
						"doctype": "Item Barcode",
						"barcode": barcode,
						"parenttype": "Item",
						"parent": item.name,
						"parentfield": "barcodes",
					}
				).insert()
			except (finergy.DuplicateEntryError, finergy.UniqueValidationError):
				continue
