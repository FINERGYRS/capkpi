# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt

import finergy
from finergy import _
from finergy.model.document import Document


class TreatmentPlanTemplate(Document):
	def validate(self):
		self.validate_age()

	def validate_age(self):
		if self.patient_age_from and self.patient_age_from < 0:
			finergy.throw(_("Patient Age From cannot be less than 0"))
		if self.patient_age_to and self.patient_age_to < 0:
			finergy.throw(_("Patient Age To cannot be less than 0"))
		if self.patient_age_to and self.patient_age_from and self.patient_age_to < self.patient_age_from:
			finergy.throw(_("Patient Age To cannot be less than Patient Age From"))
