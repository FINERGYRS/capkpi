# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.model.document import Document

# import finergy
import capkpi


class IncomeTaxSlab(Document):
	def validate(self):
		if self.company:
			self.currency = capkpi.get_company_currency(self.company)
