# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import traceback
from json import dumps

import finergy
from finergy import _, scrub
from finergy.model.document import Document
from finergy.utils import flt, nowdate
from finergy.utils.background_jobs import enqueue

from capkpi.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
)


class OpeningInvoiceCreationTool(Document):
	def onload(self):
		"""Load the Opening Invoice summary"""
		summary, max_count = self.get_opening_invoice_summary()
		self.set_onload("opening_invoices_summary", summary)
		self.set_onload("max_count", max_count)
		self.set_onload("temporary_opening_account", get_temporary_opening_account(self.company))

	def get_opening_invoice_summary(self):
		def prepare_invoice_summary(doctype, invoices):
			# add company wise sales / purchase invoice summary
			paid_amount = []
			outstanding_amount = []
			for invoice in invoices:
				company = invoice.pop("company")
				_summary = invoices_summary.get(company, {})
				_summary.update({"currency": company_wise_currency.get(company), doctype: invoice})
				invoices_summary.update({company: _summary})

				if invoice.paid_amount:
					paid_amount.append(invoice.paid_amount)
				if invoice.outstanding_amount:
					outstanding_amount.append(invoice.outstanding_amount)

			if paid_amount or outstanding_amount:
				max_count.update(
					{
						doctype: {
							"max_paid": max(paid_amount) if paid_amount else 0.0,
							"max_due": max(outstanding_amount) if outstanding_amount else 0.0,
						}
					}
				)

		invoices_summary = {}
		max_count = {}
		fields = [
			"company",
			"count(name) as total_invoices",
			"sum(outstanding_amount) as outstanding_amount",
		]
		companies = finergy.get_all("Company", fields=["name as company", "default_currency as currency"])
		if not companies:
			return None, None

		company_wise_currency = {row.company: row.currency for row in companies}
		for doctype in ["Sales Invoice", "Purchase Invoice"]:
			invoices = finergy.get_all(
				doctype, filters=dict(is_opening="Yes", docstatus=1), fields=fields, group_by="company"
			)
			prepare_invoice_summary(doctype, invoices)

		return invoices_summary, max_count

	def validate_company(self):
		if not self.company:
			finergy.throw(_("Please select the Company"))

	def set_missing_values(self, row):
		row.qty = row.qty or 1.0
		row.temporary_opening_account = row.temporary_opening_account or get_temporary_opening_account(
			self.company
		)
		row.party_type = "Customer" if self.invoice_type == "Sales" else "Supplier"
		row.item_name = row.item_name or _("Opening Invoice Item")
		row.posting_date = row.posting_date or nowdate()
		row.due_date = row.due_date or nowdate()

	def validate_mandatory_invoice_fields(self, row):
		if not finergy.db.exists(row.party_type, row.party):
			if self.create_missing_party:
				self.add_party(row.party_type, row.party)
			else:
				finergy.throw(
					_("Row #{}: {} {} does not exist.").format(
						row.idx, finergy.bold(row.party_type), finergy.bold(row.party)
					)
				)

		mandatory_error_msg = _("Row #{0}: {1} is required to create the Opening {2} Invoices")
		for d in ("Party", "Outstanding Amount", "Temporary Opening Account"):
			if not row.get(scrub(d)):
				finergy.throw(mandatory_error_msg.format(row.idx, d, self.invoice_type))

	def get_invoices(self):
		invoices = []
		for row in self.invoices:
			if not row:
				continue
			self.set_missing_values(row)
			self.validate_mandatory_invoice_fields(row)
			invoice = self.get_invoice_dict(row)
			company_details = (
				finergy.get_cached_value(
					"Company", self.company, ["default_currency", "default_letter_head"], as_dict=1
				)
				or {}
			)

			default_currency = finergy.db.get_value(row.party_type, row.party, "default_currency")

			if company_details:
				invoice.update(
					{
						"currency": default_currency or company_details.get("default_currency"),
						"letter_head": company_details.get("default_letter_head"),
					}
				)
			invoices.append(invoice)

		return invoices

	def add_party(self, party_type, party):
		party_doc = finergy.new_doc(party_type)
		if party_type == "Customer":
			party_doc.customer_name = party
		else:
			supplier_group = finergy.db.get_single_value("Buying Settings", "supplier_group")
			if not supplier_group:
				finergy.throw(_("Please Set Supplier Group in Buying Settings."))

			party_doc.supplier_name = party
			party_doc.supplier_group = supplier_group

		party_doc.flags.ignore_mandatory = True
		party_doc.save(ignore_permissions=True)

	def get_invoice_dict(self, row=None):
		def get_item_dict():
			cost_center = row.get("cost_center") or finergy.get_cached_value(
				"Company", self.company, "cost_center"
			)
			if not cost_center:
				finergy.throw(
					_("Please set the Default Cost Center in {0} company.").format(finergy.bold(self.company))
				)

			income_expense_account_field = (
				"income_account" if row.party_type == "Customer" else "expense_account"
			)
			default_uom = finergy.db.get_single_value("Stock Settings", "stock_uom") or _("Nos")
			rate = flt(row.outstanding_amount) / flt(row.qty)

			item_dict = finergy._dict(
				{
					"uom": default_uom,
					"rate": rate or 0.0,
					"qty": row.qty,
					"conversion_factor": 1.0,
					"item_name": row.item_name or "Opening Invoice Item",
					"description": row.item_name or "Opening Invoice Item",
					income_expense_account_field: row.temporary_opening_account,
					"cost_center": cost_center,
				}
			)

			for dimension in get_accounting_dimensions():
				item_dict.update({dimension: row.get(dimension)})

			return item_dict

		item = get_item_dict()

		invoice = finergy._dict(
			{
				"items": [item],
				"is_opening": "Yes",
				"set_posting_time": 1,
				"company": self.company,
				"cost_center": self.cost_center,
				"due_date": row.due_date,
				"posting_date": row.posting_date,
				finergy.scrub(row.party_type): row.party,
				"is_pos": 0,
				"doctype": "Sales Invoice" if self.invoice_type == "Sales" else "Purchase Invoice",
				"update_stock": 0,  # important: https://github.com/finergyrs/capkpi/pull/23559
				"invoice_number": row.invoice_number,
				"disable_rounded_total": 1,
			}
		)

		accounting_dimension = get_accounting_dimensions()
		for dimension in accounting_dimension:
			invoice.update({dimension: self.get(dimension) or item.get(dimension)})

		return invoice

	@finergy.whitelist()
	def make_invoices(self):
		self.validate_company()
		invoices = self.get_invoices()
		if len(invoices) < 50:
			return start_import(invoices)
		else:
			from finergy.core.page.background_jobs.background_jobs import get_info
			from finergy.utils.scheduler import is_scheduler_inactive

			if is_scheduler_inactive() and not finergy.flags.in_test:
				finergy.throw(_("Scheduler is inactive. Cannot import data."), title=_("Scheduler Inactive"))

			enqueued_jobs = [d.get("job_name") for d in get_info()]
			if self.name not in enqueued_jobs:
				enqueue(
					start_import,
					queue="default",
					timeout=6000,
					event="opening_invoice_creation",
					job_name=self.name,
					invoices=invoices,
					now=finergy.conf.developer_mode or finergy.flags.in_test,
				)


def start_import(invoices):
	errors = 0
	names = []
	for idx, d in enumerate(invoices):
		try:
			invoice_number = None
			if d.invoice_number:
				invoice_number = d.invoice_number
			publish(idx, len(invoices), d.doctype)
			doc = finergy.get_doc(d)
			doc.flags.ignore_mandatory = True
			doc.insert(set_name=invoice_number)
			doc.submit()
			finergy.db.commit()
			names.append(doc.name)
		except Exception:
			errors += 1
			finergy.db.rollback()
			message = "\n".join(
				["Data:", dumps(d, default=str, indent=4), "--" * 50, "\nException:", traceback.format_exc()]
			)
			finergy.log_error(title="Error while creating Opening Invoice", message=message)
			finergy.db.commit()
	if errors:
		finergy.msgprint(
			_("You had {} errors while creating opening invoices. Check {} for more details").format(
				errors, "<a href='/app/List/Error Log' class='variant-click'>Error Log</a>"
			),
			indicator="red",
			title=_("Error Occured"),
		)
	return names


def publish(index, total, doctype):
	if total < 5:
		return
	finergy.publish_realtime(
		"opening_invoice_creation_progress",
		dict(
			title=_("Opening Invoice Creation In Progress"),
			message=_("Creating {} out of {} {}").format(index + 1, total, doctype),
			user=finergy.session.user,
			count=index + 1,
			total=total,
		),
	)


@finergy.whitelist()
def get_temporary_opening_account(company=None):
	if not company:
		return

	accounts = finergy.get_all("Account", filters={"company": company, "account_type": "Temporary"})
	if not accounts:
		finergy.throw(_("Please add a Temporary Opening account in Chart of Accounts"))

	return accounts[0].name
