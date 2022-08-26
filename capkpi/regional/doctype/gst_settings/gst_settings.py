# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json
import os

import finergy
from finergy import _
from finergy.contacts.doctype.contact.contact import get_default_contact
from finergy.model.document import Document
from finergy.utils import date_diff, flt, get_url, nowdate


class EmailMissing(finergy.ValidationError):
	pass


class GSTSettings(Document):
	def onload(self):
		data = finergy._dict()
		data.total_addresses = finergy.db.sql(
			'''select count(*) from tabAddress where country = "India"'''
		)
		data.total_addresses_with_gstin = finergy.db.sql(
			"""select distinct count(*)
			from tabAddress where country = "India" and ifnull(gstin, '')!='' """
		)
		self.set_onload("data", data)

	def validate(self):
		# Validate duplicate accounts
		self.validate_duplicate_accounts()

	def validate_duplicate_accounts(self):
		account_list = []
		for account in self.get("gst_accounts"):
			for fieldname in ["cgst_account", "sgst_account", "igst_account", "cess_account"]:
				if account.get(fieldname) in account_list:
					finergy.throw(
						_("Account {0} appears multiple times").format(finergy.bold(account.get(fieldname)))
					)

				if account.get(fieldname):
					account_list.append(account.get(fieldname))


@finergy.whitelist()
def send_reminder():
	finergy.has_permission("GST Settings", throw=True)

	last_sent = finergy.db.get_single_value("GST Settings", "gstin_email_sent_on")
	if last_sent and date_diff(nowdate(), last_sent) < 3:
		finergy.throw(_("Please wait 3 days before resending the reminder."))

	finergy.db.set_value("GST Settings", "GST Settings", "gstin_email_sent_on", nowdate())

	# enqueue if large number of customers, suppliser
	finergy.enqueue(
		"capkpi.regional.doctype.gst_settings.gst_settings.send_gstin_reminder_to_all_parties"
	)
	finergy.msgprint(_("Email Reminders will be sent to all parties with email contacts"))


def send_gstin_reminder_to_all_parties():
	parties = []
	for address_name in finergy.db.sql(
		"""select name
		from tabAddress where country = "India" and ifnull(gstin, '')='' """
	):
		address = finergy.get_doc("Address", address_name[0])
		for link in address.links:
			party = finergy.get_doc(link.link_doctype, link.link_name)
			if link.link_doctype in ("Customer", "Supplier"):
				t = (link.link_doctype, link.link_name, address.email_id)
				if not t in parties:
					parties.append(t)

	sent_to = []
	for party in parties:
		# get email from default contact
		try:
			email_id = _send_gstin_reminder(party[0], party[1], party[2], sent_to)
			sent_to.append(email_id)
		except EmailMissing:
			pass


@finergy.whitelist()
def send_gstin_reminder(party_type, party):
	"""Send GSTIN reminder to one party (called from Customer, Supplier form)"""
	finergy.has_permission(party_type, throw=True)
	email = _send_gstin_reminder(party_type, party)
	if email:
		finergy.msgprint(_("Reminder to update GSTIN Sent"), title="Reminder sent", indicator="green")


def _send_gstin_reminder(party_type, party, default_email_id=None, sent_to=None):
	"""Send GST Reminder email"""
	email_id = finergy.db.get_value("Contact", get_default_contact(party_type, party), "email_id")
	if not email_id:
		# get email from address
		email_id = default_email_id

	if not email_id:
		finergy.throw(_("Email not found in default contact"), exc=EmailMissing)

	if sent_to and email_id in sent_to:
		return

	finergy.sendmail(
		subject="Please update your GSTIN",
		recipients=email_id,
		message="""
		<p>Hello,</p>
		<p>Please help us send you GST Ready Invoices.</p>
		<p>
			<a href="{0}?party={1}">
			Click here to update your GSTIN Number in our system
			</a>
		</p>
		<p style="color: #aaa; font-size: 11px; margin-top: 30px;">
			Get your GST Ready ERP system at <a href="https://capkpi.com">https://capkpi.com</a>
			<br>
			CapKPI is a free and open source ERP system.
		</p>
		""".format(
			os.path.join(get_url(), "/regional/india/update-gstin"), party
		),
	)

	return email_id


@finergy.whitelist()
def update_hsn_codes():
	finergy.enqueue(enqueue_update)
	finergy.msgprint(_("HSN/SAC Code sync started, this may take a few minutes..."))


def enqueue_update():
	with open(os.path.join(os.path.dirname(__file__), "hsn_code_data.json"), "r") as f:
		hsn_codes = json.loads(f.read())

	for hsn_code in hsn_codes:
		try:
			hsn_code_doc = finergy.get_doc("GST HSN Code", hsn_code.get("hsn_code"))
			hsn_code_doc.set("gst_rates", [])
			for rate in hsn_code.get("gst_rates"):
				hsn_code_doc.append(
					"gst_rates",
					{
						"minimum_taxable_value": flt(hsn_code.get("minimum_taxable_value")),
						"tax_rate": flt(rate.get("tax_rate")),
					},
				)

			hsn_code_doc.save()
		except Exception as e:
			pass