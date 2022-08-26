# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
import finergy.defaults
from finergy.model.document import Document

education_keydict = {
	# "key in defaults": "key in Global Defaults"
	"academic_year": "current_academic_year",
	"academic_term": "current_academic_term",
	"validate_batch": "validate_batch",
	"validate_course": "validate_course",
}


class EducationSettings(Document):
	def on_update(self):
		"""update defaults"""
		for key in education_keydict:
			finergy.db.set_default(key, self.get(education_keydict[key], ""))

		# clear cache
		finergy.clear_cache()

	def get_defaults(self):
		return finergy.defaults.get_defaults()

	def validate(self):
		from finergy.custom.doctype.property_setter.property_setter import make_property_setter

		if self.get("instructor_created_by") == "Naming Series":
			make_property_setter(
				"Instructor", "naming_series", "hidden", 0, "Check", validate_fields_for_doctype=False
			)
		else:
			make_property_setter(
				"Instructor", "naming_series", "hidden", 1, "Check", validate_fields_for_doctype=False
			)


def update_website_context(context):
	context["lms_enabled"] = finergy.get_doc("Education Settings").enable_lms
