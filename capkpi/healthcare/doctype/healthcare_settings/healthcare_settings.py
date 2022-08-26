# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy import _
from finergy.core.doctype.sms_settings.sms_settings import send_sms
from finergy.model.document import Document


class HealthcareSettings(Document):
	def validate(self):
		for key in [
			"collect_registration_fee",
			"link_customer_to_patient",
			"patient_name_by",
			"lab_test_approval_required",
			"create_sample_collection_for_lab_test",
			"default_medical_code_standard",
		]:
			finergy.db.set_default(key, self.get(key, ""))

		if self.collect_registration_fee:
			if self.registration_fee <= 0:
				finergy.throw(_("Registration Fee cannot be negative or zero"))

		if self.inpatient_visit_charge_item:
			validate_service_item(self.inpatient_visit_charge_item)
		if self.op_consulting_charge_item:
			validate_service_item(self.op_consulting_charge_item)
		if self.clinical_procedure_consumable_item:
			validate_service_item(self.clinical_procedure_consumable_item)


def validate_service_item(item):
	if finergy.db.get_value("Item", item, "is_stock_item"):
		finergy.throw(_("Configure a service Item for {0}").format(item))


@finergy.whitelist()
def get_sms_text(doc):
	sms_text = {}
	doc = finergy.get_doc("Lab Test", doc)
	context = {"doc": doc, "alert": doc, "comments": None}

	emailed = finergy.db.get_value("Healthcare Settings", None, "sms_emailed")
	sms_text["emailed"] = finergy.render_template(emailed, context)

	printed = finergy.db.get_value("Healthcare Settings", None, "sms_printed")
	sms_text["printed"] = finergy.render_template(printed, context)

	return sms_text


def send_registration_sms(doc):
	if finergy.db.get_single_value("Healthcare Settings", "send_registration_msg"):
		if doc.mobile:
			context = {"doc": doc, "alert": doc, "comments": None}
			if doc.get("_comments"):
				context["comments"] = json.loads(doc.get("_comments"))
			messages = finergy.db.get_single_value("Healthcare Settings", "registration_msg")
			messages = finergy.render_template(messages, context)
			number = [doc.mobile]
			send_sms(number, messages)
		else:
			finergy.msgprint(doc.name + " has no mobile number to send registration SMS", alert=True)


def get_receivable_account(company):
	receivable_account = get_account(None, "receivable_account", "Healthcare Settings", company)
	if receivable_account:
		return receivable_account

	return finergy.get_cached_value("Company", company, "default_receivable_account")


def get_income_account(practitioner, company):
	# check income account in Healthcare Practitioner
	if practitioner:
		income_account = get_account("Healthcare Practitioner", None, practitioner, company)
		if income_account:
			return income_account

	# else check income account in Healthcare Settings
	income_account = get_account(None, "income_account", "Healthcare Settings", company)
	if income_account:
		return income_account

	# else return default income account of company
	return finergy.get_cached_value("Company", company, "default_income_account")


def get_account(parent_type, parent_field, parent, company):
	if parent_type:
		return finergy.db.get_value(
			"Party Account", {"parenttype": parent_type, "parent": parent, "company": company}, "account"
		)

	if parent_field:
		return finergy.db.get_value(
			"Party Account", {"parentfield": parent_field, "parent": parent, "company": company}, "account"
		)
