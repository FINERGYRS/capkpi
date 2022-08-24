# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy.model.document import Document
from finergy.model.naming import set_name_by_naming_series


class Campaign(Document):
	def autoname(self):
		if finergy.defaults.get_global_default("campaign_naming_by") != "Naming Series":
			self.name = self.campaign_name
		else:
			set_name_by_naming_series(self)
