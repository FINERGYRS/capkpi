# Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import get_link_to_form

from capkpi.hr.utils import validate_active_employee


class EmployeeReferral(Document):
	def validate(self):
		validate_active_employee(self.referrer)
		self.set_full_name()
		self.set_referral_bonus_payment_status()

	def set_full_name(self):
		self.full_name = " ".join(filter(None, [self.first_name, self.last_name]))

	def set_referral_bonus_payment_status(self):
		if not self.is_applicable_for_referral_bonus:
			self.referral_payment_status = ""
		else:
			if not self.referral_payment_status:
				self.referral_payment_status = "Unpaid"


@finergy.whitelist()
def create_job_applicant(source_name, target_doc=None):
	emp_ref = finergy.get_doc("Employee Referral", source_name)
	# just for Api call if some set status apart from default Status
	status = emp_ref.status
	if emp_ref.status in ["Pending", "In process"]:
		status = "Open"

	job_applicant = finergy.new_doc("Job Applicant")
	job_applicant.source = "Employee Referral"
	job_applicant.employee_referral = emp_ref.name
	job_applicant.status = status
	job_applicant.designation = emp_ref.for_designation
	job_applicant.applicant_name = emp_ref.full_name
	job_applicant.email_id = emp_ref.email
	job_applicant.phone_number = emp_ref.contact_no
	job_applicant.resume_attachment = emp_ref.resume
	job_applicant.resume_link = emp_ref.resume_link
	job_applicant.save()

	finergy.msgprint(
		_("Job Applicant {0} created successfully.").format(
			get_link_to_form("Job Applicant", job_applicant.name)
		),
		title=_("Success"),
		indicator="green",
	)

	emp_ref.db_set("status", "In Process")

	return job_applicant


@finergy.whitelist()
def create_additional_salary(doc):
	import json

	from six import string_types

	if isinstance(doc, string_types):
		doc = finergy._dict(json.loads(doc))

	if not finergy.db.exists("Additional Salary", {"ref_docname": doc.name}):
		additional_salary = finergy.new_doc("Additional Salary")
		additional_salary.employee = doc.referrer
		additional_salary.company = finergy.db.get_value("Employee", doc.referrer, "company")
		additional_salary.overwrite_salary_structure_amount = 0
		additional_salary.ref_doctype = doc.doctype
		additional_salary.ref_docname = doc.name

	return additional_salary
