import finergy


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	irn_cancelled_field = finergy.db.exists(
		"Custom Field", {"dt": "Sales Invoice", "fieldname": "irn_cancelled"}
	)
	if irn_cancelled_field:
		finergy.db.set_value("Custom Field", irn_cancelled_field, "depends_on", "eval: doc.irn")
		finergy.db.set_value("Custom Field", irn_cancelled_field, "read_only", 0)
