# Copyright (c) 2020, Finergy and Contributors
# License: GNU General Public License v3. See license.txt

import finergy

from capkpi.regional.south_africa.setup import add_permissions, make_custom_fields


def execute():
	company = finergy.get_all("Company", filters={"country": "South Africa"})
	if not company:
		return

	finergy.reload_doc("regional", "doctype", "south_africa_vat_settings")
	finergy.reload_doc("regional", "report", "vat_audit_report")
	finergy.reload_doc("accounts", "doctype", "south_africa_vat_account")

	make_custom_fields()
	add_permissions()
