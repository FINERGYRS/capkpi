# Copyright (c) 2018, Finergy and contributors
# For license information, please see license.txt


from finergy.model.document import Document


class QualityAction(Document):
	def validate(self):
		self.status = "Open" if any([d.status == "Open" for d in self.resolutions]) else "Completed"
