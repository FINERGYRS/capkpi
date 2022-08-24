# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt

import finergy


def execute():
	if finergy.db.table_exists("Supplier Item Group"):
		finergy.reload_doc("selling", "doctype", "party_specific_item")
		sig = finergy.db.get_all("Supplier Item Group", fields=["name", "supplier", "item_group"])
		for item in sig:
			psi = finergy.new_doc("Party Specific Item")
			psi.party_type = "Supplier"
			psi.party = item.supplier
			psi.restrict_based_on = "Item Group"
			psi.based_on_value = item.item_group
			psi.insert()
