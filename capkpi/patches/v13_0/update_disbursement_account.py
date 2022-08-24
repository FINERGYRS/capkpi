import finergy


def execute():

	finergy.reload_doc("loan_management", "doctype", "loan_type")
	finergy.reload_doc("loan_management", "doctype", "loan")

	loan_type = finergy.qb.DocType("Loan Type")
	loan = finergy.qb.DocType("Loan")

	finergy.qb.update(loan_type).set(loan_type.disbursement_account, loan_type.payment_account).run()

	finergy.qb.update(loan).set(loan.disbursement_account, loan.payment_account).run()
