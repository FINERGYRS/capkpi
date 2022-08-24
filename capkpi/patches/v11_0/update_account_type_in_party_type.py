# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("setup", "doctype", "party_type")
	party_types = {
		"Customer": "Receivable",
		"Supplier": "Payable",
		"Employee": "Payable",
		"Member": "Receivable",
		"Shareholder": "Payable",
	}

	for party_type, account_type in party_types.items():
		finergy.db.set_value("Party Type", party_type, "account_type", account_type)
