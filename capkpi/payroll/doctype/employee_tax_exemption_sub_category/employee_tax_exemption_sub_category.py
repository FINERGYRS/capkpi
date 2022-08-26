# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import flt


class EmployeeTaxExemptionSubCategory(Document):
	def validate(self):
		category_max_amount = finergy.db.get_value(
			"Employee Tax Exemption Category", self.exemption_category, "max_amount"
		)
		if flt(self.max_amount) > flt(category_max_amount):
			finergy.throw(
				_(
					"Max Exemption Amount cannot be greater than maximum exemption amount {0} of Tax Exemption Category {1}"
				).format(category_max_amount, self.exemption_category)
			)
