# Copyright (c) 2015, ESS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import flt


class SampleCollection(Document):
	def validate(self):
		if flt(self.sample_qty) <= 0:
			finergy.throw(_("Sample Quantity cannot be negative or 0"), title=_("Invalid Quantity"))
