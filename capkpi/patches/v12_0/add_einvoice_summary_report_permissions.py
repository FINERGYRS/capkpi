import finergy


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})
	if not company:
		return

	if finergy.db.exists("Report", "E-Invoice Summary") and not finergy.db.get_value(
		"Custom Role", dict(report="E-Invoice Summary")
	):
		finergy.get_doc(
			dict(
				doctype="Custom Role",
				report="E-Invoice Summary",
				roles=[dict(role="Accounts User"), dict(role="Accounts Manager")],
			)
		).insert()
