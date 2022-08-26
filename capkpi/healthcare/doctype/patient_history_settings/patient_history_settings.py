# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import cint, cstr

from capkpi.healthcare.page.patient_history.patient_history import get_patient_history_doctypes


class PatientHistorySettings(Document):
	def validate(self):
		self.validate_submittable_doctypes()
		self.validate_date_fieldnames()

	def validate_submittable_doctypes(self):
		for entry in self.custom_doctypes:
			if not cint(finergy.db.get_value("DocType", entry.document_type, "is_submittable")):
				msg = _("Row #{0}: Document Type {1} is not submittable.").format(
					entry.idx, finergy.bold(entry.document_type)
				)
				msg += _("Patient Medical Record can only be created for submittable document types.")
				finergy.throw(msg)

	def validate_date_fieldnames(self):
		for entry in self.custom_doctypes:
			field = finergy.get_meta(entry.document_type).get_field(entry.date_fieldname)
			if not field:
				finergy.throw(
					_("Row #{0}: No such Field named {1} found in the Document Type {2}.").format(
						entry.idx, finergy.bold(entry.date_fieldname), finergy.bold(entry.document_type)
					)
				)

			if field.fieldtype not in ["Date", "Datetime"]:
				finergy.throw(
					_("Row #{0}: Field {1} in Document Type {2} is not a Date / Datetime field.").format(
						entry.idx, finergy.bold(entry.date_fieldname), finergy.bold(entry.document_type)
					)
				)

	@finergy.whitelist()
	def get_doctype_fields(self, document_type, fields):
		multicheck_fields = []
		doc_fields = finergy.get_meta(document_type).fields

		for field in doc_fields:
			if (
				field.fieldtype not in finergy.model.no_value_fields
				or field.fieldtype in finergy.model.table_fields
				and not field.hidden
			):
				multicheck_fields.append(
					{
						"label": field.label,
						"value": field.fieldname,
						"checked": 1 if field.fieldname in fields else 0,
					}
				)

		return multicheck_fields

	@finergy.whitelist()
	def get_date_field_for_dt(self, document_type):
		meta = finergy.get_meta(document_type)
		date_fields = meta.get("fields", {"fieldtype": ["in", ["Date", "Datetime"]]})

		if date_fields:
			return date_fields[0].get("fieldname")


def create_medical_record(doc, method=None):
	medical_record_required = validate_medical_record_required(doc)
	if not medical_record_required:
		return

	if finergy.db.exists("Patient Medical Record", {"reference_name": doc.name}):
		return

	subject = set_subject_field(doc)
	date_field = get_date_field(doc.doctype)
	medical_record = finergy.new_doc("Patient Medical Record")
	medical_record.patient = doc.patient
	medical_record.subject = subject
	medical_record.status = "Open"
	medical_record.communication_date = doc.get(date_field)
	medical_record.reference_doctype = doc.doctype
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)


def update_medical_record(doc, method=None):
	medical_record_required = validate_medical_record_required(doc)
	if not medical_record_required:
		return

	medical_record_id = finergy.db.exists("Patient Medical Record", {"reference_name": doc.name})

	if medical_record_id:
		subject = set_subject_field(doc)
		finergy.db.set_value("Patient Medical Record", medical_record_id[0][0], "subject", subject)
	else:
		create_medical_record(doc)


def delete_medical_record(doc, method=None):
	medical_record_required = validate_medical_record_required(doc)
	if not medical_record_required:
		return

	record = finergy.db.exists("Patient Medical Record", {"reference_name": doc.name})
	if record:
		finergy.delete_doc("Patient Medical Record", record, force=1)


def set_subject_field(doc):
	from finergy.utils.formatters import format_value

	meta = finergy.get_meta(doc.doctype)
	subject = ""
	patient_history_fields = get_patient_history_fields(doc)

	for entry in patient_history_fields:
		fieldname = entry.get("fieldname")
		if entry.get("fieldtype") == "Table" and doc.get(fieldname):
			formatted_value = get_formatted_value_for_table_field(
				doc.get(fieldname), meta.get_field(fieldname)
			)
			subject += finergy.bold(_(entry.get("label")) + ":") + "<br>" + cstr(formatted_value) + "<br>"

		else:
			if doc.get(fieldname):
				formatted_value = format_value(doc.get(fieldname), meta.get_field(fieldname), doc)
				subject += finergy.bold(_(entry.get("label")) + ":") + cstr(formatted_value) + "<br>"

	return subject


def get_date_field(doctype):
	dt = get_patient_history_config_dt(doctype)

	return finergy.db.get_value(dt, {"document_type": doctype}, "date_fieldname")


def get_patient_history_fields(doc):
	dt = get_patient_history_config_dt(doc.doctype)
	patient_history_fields = finergy.db.get_value(
		dt, {"document_type": doc.doctype}, "selected_fields"
	)

	if patient_history_fields:
		return json.loads(patient_history_fields)


def get_formatted_value_for_table_field(items, df):
	child_meta = finergy.get_meta(df.options)

	table_head = ""
	table_row = ""
	html = ""
	create_head = True
	for item in items:
		table_row += "<tr>"
		for cdf in child_meta.fields:
			if cdf.in_list_view:
				if create_head:
					table_head += "<td>" + cdf.label + "</td>"
				if item.get(cdf.fieldname):
					table_row += "<td>" + str(item.get(cdf.fieldname)) + "</td>"
				else:
					table_row += "<td></td>"
		create_head = False
		table_row += "</tr>"

	html += (
		"<table class='table table-condensed table-bordered'>" + table_head + table_row + "</table>"
	)

	return html


def get_patient_history_config_dt(doctype):
	if finergy.db.get_value("DocType", doctype, "custom"):
		return "Patient History Custom Document Type"
	else:
		return "Patient History Standard Document Type"


def validate_medical_record_required(doc):
	if (
		finergy.flags.in_patch
		or finergy.flags.in_install
		or finergy.flags.in_setup_wizard
		or get_module(doc) != "Healthcare"
	):
		return False

	if doc.doctype not in get_patient_history_doctypes():
		return False

	return True


def get_module(doc):
	module = doc.meta.module
	if not module:
		module = finergy.db.get_value("DocType", doc.doctype, "module")

	return module
