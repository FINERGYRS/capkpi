# Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


# import finergy
from finergy.model.document import Document


class LoanSecurity(Document):
	def autoname(self):
		self.name = self.loan_security_name
