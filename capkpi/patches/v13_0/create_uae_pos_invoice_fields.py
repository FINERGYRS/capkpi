# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

from capkpi.regional.united_arab_emirates.setup import make_custom_fields


def execute():
	company = finergy.get_all(
		"Company", filters={"country": ["in", ["Saudi Arabia", "United Arab Emirates"]]}
	)
	if not company:
		return

	finergy.reload_doc("accounts", "doctype", "pos_invoice")
	finergy.reload_doc("accounts", "doctype", "pos_invoice_item")

	make_custom_fields()
