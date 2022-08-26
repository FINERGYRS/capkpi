# Copyright(c) 2020, Finergy Reporting Solutions SAS (Finergy) Pvt.Ltd.and Contributors
# License: GNU General Public License v3.See license.txt


import finergy


def execute():
	finergy.reload_doc("stock", "doctype", "stock_entry")
	if finergy.db.has_column("Stock Entry", "add_to_transit"):
		finergy.db.sql(
			"""
            UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer',
            add_to_transit = 1 WHERE stock_entry_type = 'Send to Warehouse'
            """
		)

		finergy.db.sql(
			"""UPDATE `tabStock Entry` SET
            stock_entry_type = 'Material Transfer',
            purpose = 'Material Transfer'
            WHERE stock_entry_type = 'Receive at Warehouse'
            """
		)

		finergy.reload_doc("stock", "doctype", "warehouse_type")
		if not finergy.db.exists("Warehouse Type", "Transit"):
			doc = finergy.new_doc("Warehouse Type")
			doc.name = "Transit"
			doc.insert()

		finergy.reload_doc("stock", "doctype", "stock_entry_type")
		finergy.delete_doc_if_exists("Stock Entry Type", "Send to Warehouse")
		finergy.delete_doc_if_exists("Stock Entry Type", "Receive at Warehouse")
