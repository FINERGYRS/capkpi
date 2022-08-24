# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.model.meta import get_field_precision
from finergy.model.naming import set_name_from_naming_options
from finergy.utils import flt, fmt_money

import capkpi
from capkpi.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_checks_for_pl_and_bs_accounts,
)
from capkpi.accounts.doctype.accounting_dimension_filter.accounting_dimension_filter import (
	get_dimension_filter_map,
)
from capkpi.accounts.party import validate_party_frozen_disabled, validate_party_gle_currency
from capkpi.accounts.utils import get_account_currency, get_fiscal_year
from capkpi.exceptions import (
	InvalidAccountCurrency,
	InvalidAccountDimensionError,
	MandatoryAccountDimensionError,
)

exclude_from_linked_with = True


class GLEntry(Document):
	def autoname(self):
		"""
		Temporarily name doc for fast insertion
		name will be changed using autoname options (in a scheduled job)
		"""
		self.name = finergy.generate_hash(txt="", length=10)
		if self.meta.autoname == "hash":
			self.to_rename = 0

	def validate(self):
		self.flags.ignore_submit_comment = True
		self.validate_and_set_fiscal_year()
		self.pl_must_have_cost_center()

		if not self.flags.from_repost and self.voucher_type != "Period Closing Voucher":
			self.check_mandatory()
			self.validate_cost_center()
			self.check_pl_account()
			self.validate_party()
			self.validate_currency()

	def on_update(self):
		adv_adj = self.flags.adv_adj
		if not self.flags.from_repost and self.voucher_type != "Period Closing Voucher":
			self.validate_account_details(adv_adj)
			self.validate_dimensions_for_pl_and_bs()
			self.validate_allowed_dimensions()
			validate_balance_type(self.account, adv_adj)
			validate_frozen_account(self.account, adv_adj)

			if finergy.db.get_value("Account", self.account, "account_type") not in [
				"Receivable",
				"Payable",
			]:
				# Update outstanding amt on against voucher
				if (
					self.against_voucher_type in ["Journal Entry", "Sales Invoice", "Purchase Invoice", "Fees"]
					and self.against_voucher
					and self.flags.update_outstanding == "Yes"
					and not finergy.flags.is_reverse_depr_entry
				):
					update_outstanding_amt(
						self.account, self.party_type, self.party, self.against_voucher_type, self.against_voucher
					)

	def check_mandatory(self):
		mandatory = ["account", "voucher_type", "voucher_no", "company"]
		for k in mandatory:
			if not self.get(k):
				finergy.throw(_("{0} is required").format(_(self.meta.get_label(k))))

		if not (self.party_type and self.party):
			account_type = finergy.get_cached_value("Account", self.account, "account_type")
			if account_type == "Receivable":
				finergy.throw(
					_("{0} {1}: Customer is required against Receivable account {2}").format(
						self.voucher_type, self.voucher_no, self.account
					)
				)
			elif account_type == "Payable":
				finergy.throw(
					_("{0} {1}: Supplier is required against Payable account {2}").format(
						self.voucher_type, self.voucher_no, self.account
					)
				)

		# Zero value transaction is not allowed
		if not (flt(self.debit, self.precision("debit")) or flt(self.credit, self.precision("credit"))):
			finergy.throw(
				_("{0} {1}: Either debit or credit amount is required for {2}").format(
					self.voucher_type, self.voucher_no, self.account
				)
			)

	def pl_must_have_cost_center(self):
		"""Validate that profit and loss type account GL entries have a cost center."""

		if self.cost_center or self.voucher_type == "Period Closing Voucher":
			return

		if finergy.get_cached_value("Account", self.account, "report_type") == "Profit and Loss":
			msg = _("{0} {1}: Cost Center is required for 'Profit and Loss' account {2}.").format(
				self.voucher_type, self.voucher_no, self.account
			)
			msg += " "
			msg += _(
				"Please set the cost center field in {0} or setup a default Cost Center for the Company."
			).format(self.voucher_type)

			finergy.throw(msg, title=_("Missing Cost Center"))

	def validate_dimensions_for_pl_and_bs(self):
		account_type = finergy.db.get_value("Account", self.account, "report_type")

		for dimension in get_checks_for_pl_and_bs_accounts():
			if (
				account_type == "Profit and Loss"
				and self.company == dimension.company
				and dimension.mandatory_for_pl
				and not dimension.disabled
			):
				if not self.get(dimension.fieldname):
					finergy.throw(
						_("Accounting Dimension <b>{0}</b> is required for 'Profit and Loss' account {1}.").format(
							dimension.label, self.account
						)
					)

			if (
				account_type == "Balance Sheet"
				and self.company == dimension.company
				and dimension.mandatory_for_bs
				and not dimension.disabled
			):
				if not self.get(dimension.fieldname):
					finergy.throw(
						_("Accounting Dimension <b>{0}</b> is required for 'Balance Sheet' account {1}.").format(
							dimension.label, self.account
						)
					)

	def validate_allowed_dimensions(self):
		dimension_filter_map = get_dimension_filter_map()
		for key, value in dimension_filter_map.items():
			dimension = key[0]
			account = key[1]

			if self.account == account:
				if value["is_mandatory"] and not self.get(dimension):
					finergy.throw(
						_("{0} is mandatory for account {1}").format(
							finergy.bold(finergy.unscrub(dimension)), finergy.bold(self.account)
						),
						MandatoryAccountDimensionError,
					)

				if value["allow_or_restrict"] == "Allow":
					if self.get(dimension) and self.get(dimension) not in value["allowed_dimensions"]:
						finergy.throw(
							_("Invalid value {0} for {1} against account {2}").format(
								finergy.bold(self.get(dimension)),
								finergy.bold(finergy.unscrub(dimension)),
								finergy.bold(self.account),
							),
							InvalidAccountDimensionError,
						)
				else:
					if self.get(dimension) and self.get(dimension) in value["allowed_dimensions"]:
						finergy.throw(
							_("Invalid value {0} for {1} against account {2}").format(
								finergy.bold(self.get(dimension)),
								finergy.bold(finergy.unscrub(dimension)),
								finergy.bold(self.account),
							),
							InvalidAccountDimensionError,
						)

	def check_pl_account(self):
		if (
			self.is_opening == "Yes"
			and finergy.db.get_value("Account", self.account, "report_type") == "Profit and Loss"
			and not self.is_cancelled
		):
			finergy.throw(
				_("{0} {1}: 'Profit and Loss' type account {2} not allowed in Opening Entry").format(
					self.voucher_type, self.voucher_no, self.account
				)
			)

	def validate_account_details(self, adv_adj):
		"""Account must be ledger, active and not freezed"""

		ret = finergy.db.sql(
			"""select is_group, docstatus, company
			from tabAccount where name=%s""",
			self.account,
			as_dict=1,
		)[0]

		if ret.is_group == 1:
			finergy.throw(
				_(
					"""{0} {1}: Account {2} is a Group Account and group accounts cannot be used in transactions"""
				).format(self.voucher_type, self.voucher_no, self.account)
			)

		if ret.docstatus == 2:
			finergy.throw(
				_("{0} {1}: Account {2} is inactive").format(self.voucher_type, self.voucher_no, self.account)
			)

		if ret.company != self.company:
			finergy.throw(
				_("{0} {1}: Account {2} does not belong to Company {3}").format(
					self.voucher_type, self.voucher_no, self.account, self.company
				)
			)

	def validate_cost_center(self):
		if not self.cost_center:
			return

		is_group, company = finergy.get_cached_value(
			"Cost Center", self.cost_center, ["is_group", "company"]
		)

		if company != self.company:
			finergy.throw(
				_("{0} {1}: Cost Center {2} does not belong to Company {3}").format(
					self.voucher_type, self.voucher_no, self.cost_center, self.company
				)
			)

		if self.voucher_type != "Period Closing Voucher" and is_group:
			finergy.throw(
				_(
					"""{0} {1}: Cost Center {2} is a group cost center and group cost centers cannot be used in transactions"""
				).format(self.voucher_type, self.voucher_no, finergy.bold(self.cost_center))
			)

	def validate_party(self):
		validate_party_frozen_disabled(self.party_type, self.party)

	def validate_currency(self):
		company_currency = capkpi.get_company_currency(self.company)
		account_currency = get_account_currency(self.account)

		if not self.account_currency:
			self.account_currency = account_currency or company_currency

		if account_currency != self.account_currency:
			finergy.throw(
				_("{0} {1}: Accounting Entry for {2} can only be made in currency: {3}").format(
					self.voucher_type, self.voucher_no, self.account, (account_currency or company_currency)
				),
				InvalidAccountCurrency,
			)

		if self.party_type and self.party:
			validate_party_gle_currency(self.party_type, self.party, self.company, self.account_currency)

	def validate_and_set_fiscal_year(self):
		if not self.fiscal_year:
			self.fiscal_year = get_fiscal_year(self.posting_date, company=self.company)[0]

	def on_cancel(self):
		msg = _("Individual GL Entry cannot be cancelled.")
		msg += "<br>" + _("Please cancel related transaction.")
		finergy.throw(msg)


def validate_balance_type(account, adv_adj=False):
	if not adv_adj and account:
		balance_must_be = finergy.db.get_value("Account", account, "balance_must_be")
		if balance_must_be:
			balance = finergy.db.sql(
				"""select sum(debit) - sum(credit)
				from `tabGL Entry` where account = %s""",
				account,
			)[0][0]

			if (balance_must_be == "Debit" and flt(balance) < 0) or (
				balance_must_be == "Credit" and flt(balance) > 0
			):
				finergy.throw(
					_("Balance for Account {0} must always be {1}").format(account, _(balance_must_be))
				)


def update_outstanding_amt(
	account, party_type, party, against_voucher_type, against_voucher, on_cancel=False
):
	if party_type and party:
		party_condition = " and party_type={0} and party={1}".format(
			finergy.db.escape(party_type), finergy.db.escape(party)
		)
	else:
		party_condition = ""

	if against_voucher_type == "Sales Invoice":
		party_account = finergy.db.get_value(against_voucher_type, against_voucher, "debit_to")
		account_condition = "and account in ({0}, {1})".format(
			finergy.db.escape(account), finergy.db.escape(party_account)
		)
	else:
		account_condition = " and account = {0}".format(finergy.db.escape(account))

	# get final outstanding amt
	bal = flt(
		finergy.db.sql(
			"""
		select sum(debit_in_account_currency) - sum(credit_in_account_currency)
		from `tabGL Entry`
		where against_voucher_type=%s and against_voucher=%s
		and voucher_type != 'Invoice Discounting'
		{0} {1}""".format(
				party_condition, account_condition
			),
			(against_voucher_type, against_voucher),
		)[0][0]
		or 0.0
	)

	if against_voucher_type == "Purchase Invoice":
		bal = -bal
	elif against_voucher_type == "Journal Entry":
		against_voucher_amount = flt(
			finergy.db.sql(
				"""
			select sum(debit_in_account_currency) - sum(credit_in_account_currency)
			from `tabGL Entry` where voucher_type = 'Journal Entry' and voucher_no = %s
			and account = %s and (against_voucher is null or against_voucher='') {0}""".format(
					party_condition
				),
				(against_voucher, account),
			)[0][0]
		)

		if not against_voucher_amount:
			finergy.throw(
				_("Against Journal Entry {0} is already adjusted against some other voucher").format(
					against_voucher
				)
			)

		bal = against_voucher_amount + bal
		if against_voucher_amount < 0:
			bal = -bal

		# Validation : Outstanding can not be negative for JV
		if bal < 0 and not on_cancel:
			finergy.throw(
				_("Outstanding for {0} cannot be less than zero ({1})").format(against_voucher, fmt_money(bal))
			)

	if against_voucher_type in ["Sales Invoice", "Purchase Invoice", "Fees"]:
		ref_doc = finergy.get_doc(against_voucher_type, against_voucher)

		# Didn't use db_set for optimization purpose
		ref_doc.outstanding_amount = bal
		finergy.db.set_value(against_voucher_type, against_voucher, "outstanding_amount", bal)

		ref_doc.set_status(update=True)


def validate_frozen_account(account, adv_adj=None):
	frozen_account = finergy.get_cached_value("Account", account, "freeze_account")
	if frozen_account == "Yes" and not adv_adj:
		frozen_accounts_modifier = finergy.db.get_value(
			"Accounts Settings", None, "frozen_accounts_modifier"
		)

		if not frozen_accounts_modifier:
			finergy.throw(_("Account {0} is frozen").format(account))
		elif frozen_accounts_modifier not in finergy.get_roles():
			finergy.throw(_("Not authorized to edit frozen Account {0}").format(account))


def update_against_account(voucher_type, voucher_no):
	entries = finergy.db.get_all(
		"GL Entry",
		filters={"voucher_type": voucher_type, "voucher_no": voucher_no},
		fields=["name", "party", "against", "debit", "credit", "account", "company"],
	)

	if not entries:
		return
	company_currency = capkpi.get_company_currency(entries[0].company)
	precision = get_field_precision(finergy.get_meta("GL Entry").get_field("debit"), company_currency)

	accounts_debited, accounts_credited = [], []
	for d in entries:
		if flt(d.debit, precision) > 0:
			accounts_debited.append(d.party or d.account)
		if flt(d.credit, precision) > 0:
			accounts_credited.append(d.party or d.account)

	for d in entries:
		if flt(d.debit, precision) > 0:
			new_against = ", ".join(list(set(accounts_credited)))
		if flt(d.credit, precision) > 0:
			new_against = ", ".join(list(set(accounts_debited)))

		if d.against != new_against:
			finergy.db.set_value("GL Entry", d.name, "against", new_against)


def on_doctype_update():
	finergy.db.add_index("GL Entry", ["against_voucher_type", "against_voucher"])
	finergy.db.add_index("GL Entry", ["voucher_type", "voucher_no"])


def rename_gle_sle_docs():
	for doctype in ["GL Entry", "Stock Ledger Entry"]:
		rename_temporarily_named_docs(doctype)


def rename_temporarily_named_docs(doctype):
	"""Rename temporarily named docs using autoname options"""
	docs_to_rename = finergy.get_all(doctype, {"to_rename": "1"}, order_by="creation", limit=50000)
	for doc in docs_to_rename:
		oldname = doc.name
		set_name_from_naming_options(finergy.get_meta(doctype).autoname, doc)
		newname = doc.name
		finergy.db.sql(
			"UPDATE `tab{}` SET name = %s, to_rename = 0 where name = %s".format(doctype),
			(newname, oldname),
			auto_commit=True,
		)
