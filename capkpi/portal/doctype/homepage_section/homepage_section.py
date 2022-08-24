# Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.model.document import Document
from finergy.utils import cint


class HomepageSection(Document):
	@property
	def column_value(self):
		return cint(12 / cint(self.no_of_columns or 3))
