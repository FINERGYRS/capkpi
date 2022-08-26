import finergy


def execute():
	finergy.reload_doc("setup", "doctype", "company")

	companies = finergy.get_all("Company", fields=["name", "default_payable_account"])

	for company in companies:
		if company.default_payable_account is not None:
			finergy.db.set_value(
				"Company",
				company.name,
				"default_expense_claim_payable_account",
				company.default_payable_account,
			)
