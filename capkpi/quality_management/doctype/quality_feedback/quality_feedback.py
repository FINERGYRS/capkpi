# Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class QualityFeedback(Document):
	@finergy.whitelist()
	def set_parameters(self):
		if self.template and not getattr(self, "parameters", []):
			for d in finergy.get_doc("Quality Feedback Template", self.template).parameters:
				self.append("parameters", dict(parameter=d.parameter, rating=1))

	def validate(self):
		if not self.document_name:
			self.document_type = "User"
			self.document_name = finergy.session.user
		self.set_parameters()
