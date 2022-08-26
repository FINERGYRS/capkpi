import finergy


def execute():
	finergy.reload_doc("loan_management", "doctype", "loan")
	loan = finergy.qb.DocType("Loan")

	for company in finergy.get_all("Company", pluck="name"):
		default_cost_center = finergy.db.get_value("Company", company, "cost_center")
		finergy.qb.update(loan).set(loan.cost_center, default_cost_center).where(
			loan.company == company
		).run()
