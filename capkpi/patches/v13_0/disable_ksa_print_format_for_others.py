# Copyright (c) 2020, Wahni Green Technologies and Contributors
# License: GNU General Public License v3. See license.txt

import finergy

from capkpi.regional.saudi_arabia.setup import add_print_formats


def execute():
	company = finergy.get_all("Company", filters={"country": "Saudi Arabia"})
	if company:
		add_print_formats()
		return

	if finergy.db.exists("DocType", "Print Format"):
		finergy.reload_doc("regional", "print_format", "ksa_vat_invoice", force=True)
		finergy.reload_doc("regional", "print_format", "ksa_pos_invoice", force=True)
		for d in ("KSA VAT Invoice", "KSA POS Invoice"):
			finergy.db.set_value("Print Format", d, "disabled", 1)
