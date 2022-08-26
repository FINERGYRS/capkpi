# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy import _
from finergy.model.document import Document


class EInvoiceSettings(Document):
	def validate(self):
		if self.enable and not self.credentials:
			finergy.throw(_("You must add atleast one credentials to be able to use E Invoicing."))
