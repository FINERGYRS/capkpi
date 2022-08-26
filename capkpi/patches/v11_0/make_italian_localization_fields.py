# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

from capkpi.regional.italy import state_codes
from capkpi.regional.italy.setup import make_custom_fields, setup_report


def execute():
	company = finergy.get_all("Company", filters={"country": "Italy"})
	if not company:
		return

	finergy.reload_doc("regional", "report", "electronic_invoice_register")
	make_custom_fields()
	setup_report()

	# Set state codes
	condition = ""
	for state, code in state_codes.items():
		condition += " when {0} then {1}".format(finergy.db.escape(state), finergy.db.escape(code))

	if condition:
		condition = "state_code = (case state {0} end),".format(condition)

	finergy.db.sql(
		"""
		UPDATE tabAddress set {condition} country_code = UPPER(ifnull((select code
			from `tabCountry` where name = `tabAddress`.country), ''))
			where country_code is null and state_code is null
	""".format(
			condition=condition
		)
	)

	finergy.db.sql(
		"""
		UPDATE `tabSales Invoice Item` si, `tabSales Order` so
			set si.customer_po_no = so.po_no, si.customer_po_date = so.po_date
		WHERE
			si.sales_order = so.name and so.po_no is not null
	"""
	)
