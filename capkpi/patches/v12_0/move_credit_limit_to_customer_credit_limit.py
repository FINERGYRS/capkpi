# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	"""Move credit limit and bypass credit limit to the child table of customer credit limit"""
	finergy.reload_doc("Selling", "doctype", "Customer Credit Limit")
	finergy.reload_doc("Selling", "doctype", "Customer")
	finergy.reload_doc("Setup", "doctype", "Customer Group")

	if finergy.db.a_row_exists("Customer Credit Limit"):
		return

	move_credit_limit_to_child_table()


def move_credit_limit_to_child_table():
	"""maps data from old field to the new field in the child table"""

	companies = finergy.get_all("Company", "name")
	for doctype in ("Customer", "Customer Group"):
		fields = ""
		if doctype == "Customer" and finergy.db.has_column(
			"Customer", "bypass_credit_limit_check_at_sales_order"
		):
			fields = ", bypass_credit_limit_check_at_sales_order"

		credit_limit_records = finergy.db.sql(
			"""
			SELECT name, credit_limit {0}
			FROM `tab{1}` where credit_limit > 0
		""".format(
				fields, doctype
			),
			as_dict=1,
		)  # nosec

		for record in credit_limit_records:
			doc = finergy.get_doc(doctype, record.name)
			for company in companies:
				row = finergy._dict({"credit_limit": record.credit_limit, "company": company.name})
				if doctype == "Customer":
					row.bypass_credit_limit_check = record.bypass_credit_limit_check_at_sales_order

				doc.append("credit_limits", row)

			for row in doc.credit_limits:
				row.db_insert()
