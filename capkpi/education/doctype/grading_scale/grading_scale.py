# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import cint


class GradingScale(Document):
	def validate(self):
		thresholds = []
		for d in self.intervals:
			if d.threshold in thresholds:
				finergy.throw(_("Treshold {0}% appears more than once").format(d.threshold))
			else:
				thresholds.append(cint(d.threshold))
		if 0 not in thresholds:
			finergy.throw(_("Please define grade for Threshold 0%"))
