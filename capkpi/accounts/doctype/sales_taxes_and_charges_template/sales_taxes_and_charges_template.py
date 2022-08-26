# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import flt

from capkpi.controllers.accounts_controller import (
	validate_account_head,
	validate_cost_center,
	validate_inclusive_tax,
	validate_taxes_and_charges,
)


class SalesTaxesandChargesTemplate(Document):
	def validate(self):
		valdiate_taxes_and_charges_template(self)

	def autoname(self):
		if self.company and self.title:
			abbr = finergy.get_cached_value("Company", self.company, "abbr")
			self.name = "{0} - {1}".format(self.title, abbr)

	def set_missing_values(self):
		for data in self.taxes:
			if data.charge_type == "On Net Total" and flt(data.rate) == 0.0:
				data.rate = finergy.db.get_value("Account", data.account_head, "tax_rate")


def valdiate_taxes_and_charges_template(doc):
	# default should not be disabled
	# if not doc.is_default and not finergy.get_all(doc.doctype, filters={"is_default": 1}):
	# 	doc.is_default = 1

	if doc.is_default == 1:
		finergy.db.sql(
			"""update `tab{0}` set is_default = 0
			where is_default = 1 and name != %s and company = %s""".format(
				doc.doctype
			),
			(doc.name, doc.company),
		)

	validate_disabled(doc)

	# Validate with existing taxes and charges template for unique tax category
	validate_for_tax_category(doc)

	for tax in doc.get("taxes"):
		validate_taxes_and_charges(tax)
		validate_account_head(tax.idx, tax.account_head, doc.company)
		validate_cost_center(tax, doc)
		validate_inclusive_tax(tax, doc)


def validate_disabled(doc):
	if doc.is_default and doc.disabled:
		finergy.throw(_("Disabled template must not be default template"))


def validate_for_tax_category(doc):
	if not doc.tax_category:
		return

	if finergy.db.exists(
		doc.doctype,
		{
			"company": doc.company,
			"tax_category": doc.tax_category,
			"disabled": 0,
			"name": ["!=", doc.name],
		},
	):
		finergy.throw(
			_(
				"A template with tax category {0} already exists. Only one template is allowed with each tax category"
			).format(finergy.bold(doc.tax_category))
		)
