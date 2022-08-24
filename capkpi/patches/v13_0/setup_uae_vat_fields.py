# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt

import finergy

from capkpi.regional.united_arab_emirates.setup import setup


def execute():
	company = finergy.get_all("Company", filters={"country": "United Arab Emirates"})
	if not company:
		return

	finergy.reload_doc("regional", "report", "uae_vat_201")
	finergy.reload_doc("regional", "doctype", "uae_vat_settings")
	finergy.reload_doc("regional", "doctype", "uae_vat_account")

	setup()
