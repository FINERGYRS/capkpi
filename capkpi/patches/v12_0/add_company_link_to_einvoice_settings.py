import finergy


def execute():
	company = finergy.get_all("Company", filters={"country": "India"})

	if not company:
		return

	finergy.reload_doc("regional", "doctype", "e_invoice_user")
	if not finergy.db.count("E Invoice User"):
		return

	for creds in finergy.db.get_all("E Invoice User", fields=["name", "gstin"]):
		company_name = finergy.db.sql(
			"""
			select dl.link_name from `tabAddress` a, `tabDynamic Link` dl
			where a.gstin = %s and dl.parent = a.name and dl.link_doctype = 'Company'
		""",
			(creds.get("gstin")),
		)
		if company_name and len(company_name) > 0:
			finergy.db.set_value("E Invoice User", creds.get("name"), "company", company_name[0][0])
