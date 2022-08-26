# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.model.document import Document


class MedicalCode(Document):
	def autoname(self):
		self.name = self.medical_code_standard + " " + self.code
