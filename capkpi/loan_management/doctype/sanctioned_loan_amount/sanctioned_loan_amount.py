# Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class SanctionedLoanAmount(Document):
	def validate(self):
		sanctioned_doc = finergy.db.exists(
			"Sanctioned Loan Amount", {"applicant": self.applicant, "company": self.company}
		)

		if sanctioned_doc and sanctioned_doc != self.name:
			finergy.throw(
				_("Sanctioned Loan Amount already exists for {0} against company {1}").format(
					finergy.bold(self.applicant), finergy.bold(self.company)
				)
			)
