# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy.model.document import Document


class CRMSettings(Document):
	def validate(self):
		finergy.db.set_default("campaign_naming_by", self.get("campaign_naming_by", ""))
