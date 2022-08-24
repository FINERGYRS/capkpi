# Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class LoanType(Document):
	def validate(self):
		self.validate_accounts()

	def validate_accounts(self):
		for fieldname in [
			"payment_account",
			"loan_account",
			"interest_income_account",
			"penalty_income_account",
		]:
			company = finergy.get_value("Account", self.get(fieldname), "company")

			if company and company != self.company:
				finergy.throw(
					_("Account {0} does not belong to company {1}").format(
						finergy.bold(self.get(fieldname)), finergy.bold(self.company)
					)
				)

		if self.get("loan_account") == self.get("payment_account"):
			finergy.throw(_("Loan Account and Payment Account cannot be same"))
