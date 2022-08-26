# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import functools
import json
import os

import finergy
import finergy.defaults
from finergy import _
from finergy.cache_manager import clear_defaults_cache
from finergy.contacts.address_and_contact import load_address_and_contact
from finergy.custom.doctype.property_setter.property_setter import make_property_setter
from finergy.utils import cint, formatdate, get_timestamp, today
from finergy.utils.nestedset import NestedSet
from past.builtins import cmp

from capkpi.accounts.doctype.account.account import get_account_currency
from capkpi.setup.setup_wizard.operations.taxes_setup import setup_taxes_and_charges


class Company(NestedSet):
	nsm_parent_field = "parent_company"

	def onload(self):
		load_address_and_contact(self, "company")

	@finergy.whitelist()
	def check_if_transactions_exist(self):
		exists = False
		for doctype in [
			"Sales Invoice",
			"Delivery Note",
			"Sales Order",
			"Quotation",
			"Purchase Invoice",
			"Purchase Receipt",
			"Purchase Order",
			"Supplier Quotation",
		]:
			if finergy.db.sql(
				"""select name from `tab%s` where company=%s and docstatus=1
					limit 1"""
				% (doctype, "%s"),
				self.name,
			):
				exists = True
				break

		return exists

	def validate(self):
		self.update_default_account = False
		if self.is_new():
			self.update_default_account = True

		self.validate_abbr()
		self.validate_default_accounts()
		self.validate_currency()
		self.validate_coa_input()
		self.validate_perpetual_inventory()
		self.validate_provisional_account_for_non_stock_items()
		self.check_country_change()
		self.check_parent_changed()
		self.set_chart_of_accounts()
		self.validate_parent_company()

	def validate_abbr(self):
		if not self.abbr:
			self.abbr = "".join(c[0] for c in self.company_name.split()).upper()

		self.abbr = self.abbr.strip()

		# if self.get('__islocal') and len(self.abbr) > 5:
		# 	finergy.throw(_("Abbreviation cannot have more than 5 characters"))

		if not self.abbr.strip():
			finergy.throw(_("Abbreviation is mandatory"))

		if finergy.db.sql(
			"select abbr from tabCompany where name!=%s and abbr=%s", (self.name, self.abbr)
		):
			finergy.throw(_("Abbreviation already used for another company"))

	@finergy.whitelist()
	def create_default_tax_template(self):
		setup_taxes_and_charges(self.name, self.country)

	def validate_default_accounts(self):
		accounts = [
			["Default Bank Account", "default_bank_account"],
			["Default Cash Account", "default_cash_account"],
			["Default Receivable Account", "default_receivable_account"],
			["Default Payable Account", "default_payable_account"],
			["Default Expense Account", "default_expense_account"],
			["Default Income Account", "default_income_account"],
			["Stock Received But Not Billed Account", "stock_received_but_not_billed"],
			["Stock Adjustment Account", "stock_adjustment_account"],
			["Expense Included In Valuation Account", "expenses_included_in_valuation"],
			["Default Payroll Payable Account", "default_payroll_payable_account"],
		]

		for account in accounts:
			if self.get(account[1]):
				for_company = finergy.db.get_value("Account", self.get(account[1]), "company")
				if for_company != self.name:
					finergy.throw(
						_("Account {0} does not belong to company: {1}").format(self.get(account[1]), self.name)
					)

				if get_account_currency(self.get(account[1])) != self.default_currency:
					error_message = _(
						"{0} currency must be same as company's default currency. Please select another account."
					).format(finergy.bold(account[0]))
					finergy.throw(error_message)

	def validate_currency(self):
		if self.is_new():
			return
		self.previous_default_currency = finergy.get_cached_value(
			"Company", self.name, "default_currency"
		)
		if (
			self.default_currency
			and self.previous_default_currency
			and self.default_currency != self.previous_default_currency
			and self.check_if_transactions_exist()
		):
			finergy.throw(
				_(
					"Cannot change company's default currency, because there are existing transactions. Transactions must be cancelled to change the default currency."
				)
			)

	def on_update(self):
		NestedSet.on_update(self)
		if not finergy.db.sql(
			"""select name from tabAccount
				where company=%s and docstatus<2 limit 1""",
			self.name,
		):
			if not finergy.local.flags.ignore_chart_of_accounts:
				finergy.flags.country_change = True
				self.create_default_accounts()
				self.create_default_warehouses()

		if not finergy.db.get_value("Cost Center", {"is_group": 0, "company": self.name}):
			self.create_default_cost_center()

		if finergy.flags.country_change:
			install_country_fixtures(self.name, self.country)
			self.create_default_tax_template()

		if not finergy.db.get_value("Department", {"company": self.name}):
			from capkpi.setup.setup_wizard.operations.install_fixtures import install_post_company_fixtures

			install_post_company_fixtures(finergy._dict({"company_name": self.name}))

		if not finergy.local.flags.ignore_chart_of_accounts:
			self.set_default_accounts()
			if self.default_cash_account:
				self.set_mode_of_payment_account()

		if self.default_currency:
			finergy.db.set_value("Currency", self.default_currency, "enabled", 1)

		if (
			hasattr(finergy.local, "enable_perpetual_inventory")
			and self.name in finergy.local.enable_perpetual_inventory
		):
			finergy.local.enable_perpetual_inventory[self.name] = self.enable_perpetual_inventory

		if finergy.flags.parent_company_changed:
			from finergy.utils.nestedset import rebuild_tree

			rebuild_tree("Company", "parent_company")

		finergy.clear_cache()

	def create_default_warehouses(self):
		for wh_detail in [
			{"warehouse_name": _("All Warehouses"), "is_group": 1},
			{"warehouse_name": _("Stores"), "is_group": 0},
			{"warehouse_name": _("Work In Progress"), "is_group": 0},
			{"warehouse_name": _("Finished Goods"), "is_group": 0},
			{"warehouse_name": _("Goods In Transit"), "is_group": 0, "warehouse_type": "Transit"},
		]:

			if not finergy.db.exists(
				"Warehouse", "{0} - {1}".format(wh_detail["warehouse_name"], self.abbr)
			):
				warehouse = finergy.get_doc(
					{
						"doctype": "Warehouse",
						"warehouse_name": wh_detail["warehouse_name"],
						"is_group": wh_detail["is_group"],
						"company": self.name,
						"parent_warehouse": "{0} - {1}".format(_("All Warehouses"), self.abbr)
						if not wh_detail["is_group"]
						else "",
						"warehouse_type": wh_detail["warehouse_type"] if "warehouse_type" in wh_detail else None,
					}
				)
				warehouse.flags.ignore_permissions = True
				warehouse.flags.ignore_mandatory = True
				warehouse.insert()

	def create_default_accounts(self):
		from capkpi.accounts.doctype.account.chart_of_accounts.chart_of_accounts import create_charts

		finergy.local.flags.ignore_root_company_validation = True
		create_charts(self.name, self.chart_of_accounts, self.existing_company)

		finergy.db.set(
			self,
			"default_receivable_account",
			finergy.db.get_value(
				"Account", {"company": self.name, "account_type": "Receivable", "is_group": 0}
			),
		)
		finergy.db.set(
			self,
			"default_payable_account",
			finergy.db.get_value(
				"Account", {"company": self.name, "account_type": "Payable", "is_group": 0}
			),
		)

	def validate_coa_input(self):
		if self.create_chart_of_accounts_based_on == "Existing Company":
			self.chart_of_accounts = None
			if not self.existing_company:
				finergy.throw(_("Please select Existing Company for creating Chart of Accounts"))

		else:
			self.existing_company = None
			self.create_chart_of_accounts_based_on = "Standard Template"
			if not self.chart_of_accounts:
				self.chart_of_accounts = "Standard"

	def validate_perpetual_inventory(self):
		if not self.get("__islocal"):
			if cint(self.enable_perpetual_inventory) == 1 and not self.default_inventory_account:
				finergy.msgprint(
					_("Set default inventory account for perpetual inventory"), alert=True, indicator="orange"
				)

	def validate_provisional_account_for_non_stock_items(self):
		if not self.get("__islocal"):
			if (
				cint(self.enable_provisional_accounting_for_non_stock_items) == 1
				and not self.default_provisional_account
			):
				finergy.throw(
					_("Set default {0} account for non stock items").format(finergy.bold("Provisional Account"))
				)

			make_property_setter(
				"Purchase Receipt",
				"provisional_expense_account",
				"hidden",
				not self.enable_provisional_accounting_for_non_stock_items,
				"Check",
				validate_fields_for_doctype=False,
			)

	def check_country_change(self):
		finergy.flags.country_change = False

		if not self.is_new() and self.country != finergy.get_cached_value(
			"Company", self.name, "country"
		):
			finergy.flags.country_change = True

	def set_chart_of_accounts(self):
		"""If parent company is set, chart of accounts will be based on that company"""
		if self.parent_company:
			self.create_chart_of_accounts_based_on = "Existing Company"
			self.existing_company = self.parent_company

	def validate_parent_company(self):
		if self.parent_company:
			is_group = finergy.get_value("Company", self.parent_company, "is_group")

			if not is_group:
				finergy.throw(_("Parent Company must be a group company"))

	def set_default_accounts(self):
		default_accounts = {
			"default_cash_account": "Cash",
			"default_bank_account": "Bank",
			"round_off_account": "Round Off",
			"accumulated_depreciation_account": "Accumulated Depreciation",
			"depreciation_expense_account": "Depreciation",
			"capital_work_in_progress_account": "Capital Work in Progress",
			"asset_received_but_not_billed": "Asset Received But Not Billed",
			"expenses_included_in_asset_valuation": "Expenses Included In Asset Valuation",
		}

		if self.enable_perpetual_inventory:
			default_accounts.update(
				{
					"stock_received_but_not_billed": "Stock Received But Not Billed",
					"default_inventory_account": "Stock",
					"stock_adjustment_account": "Stock Adjustment",
					"expenses_included_in_valuation": "Expenses Included In Valuation",
					"default_expense_account": "Cost of Goods Sold",
				}
			)

		if self.update_default_account:
			for default_account in default_accounts:
				self._set_default_account(default_account, default_accounts.get(default_account))

		if not self.default_income_account:
			income_account = finergy.db.get_value(
				"Account", {"account_name": _("Sales"), "company": self.name, "is_group": 0}
			)

			if not income_account:
				income_account = finergy.db.get_value(
					"Account", {"account_name": _("Sales Account"), "company": self.name}
				)

			self.db_set("default_income_account", income_account)

		if not self.default_payable_account:
			self.db_set("default_payable_account", self.default_payable_account)

		if not self.default_payroll_payable_account:
			payroll_payable_account = finergy.db.get_value(
				"Account", {"account_name": _("Payroll Payable"), "company": self.name, "is_group": 0}
			)

			self.db_set("default_payroll_payable_account", payroll_payable_account)

		if not self.default_employee_advance_account:
			employe_advance_account = finergy.db.get_value(
				"Account", {"account_name": _("Employee Advances"), "company": self.name, "is_group": 0}
			)

			self.db_set("default_employee_advance_account", employe_advance_account)

		if not self.write_off_account:
			write_off_acct = finergy.db.get_value(
				"Account", {"account_name": _("Write Off"), "company": self.name, "is_group": 0}
			)

			self.db_set("write_off_account", write_off_acct)

		if not self.exchange_gain_loss_account:
			exchange_gain_loss_acct = finergy.db.get_value(
				"Account", {"account_name": _("Exchange Gain/Loss"), "company": self.name, "is_group": 0}
			)

			self.db_set("exchange_gain_loss_account", exchange_gain_loss_acct)

		if not self.disposal_account:
			disposal_acct = finergy.db.get_value(
				"Account",
				{"account_name": _("Gain/Loss on Asset Disposal"), "company": self.name, "is_group": 0},
			)

			self.db_set("disposal_account", disposal_acct)

	def _set_default_account(self, fieldname, account_type):
		if self.get(fieldname):
			return

		account = finergy.db.get_value(
			"Account", {"account_type": account_type, "is_group": 0, "company": self.name}
		)

		if account:
			self.db_set(fieldname, account)

	def set_mode_of_payment_account(self):
		cash = finergy.db.get_value("Mode of Payment", {"type": "Cash"}, "name")
		if (
			cash
			and self.default_cash_account
			and not finergy.db.get_value("Mode of Payment Account", {"company": self.name, "parent": cash})
		):
			mode_of_payment = finergy.get_doc("Mode of Payment", cash, for_update=True)
			mode_of_payment.append(
				"accounts", {"company": self.name, "default_account": self.default_cash_account}
			)
			mode_of_payment.save(ignore_permissions=True)

	def create_default_cost_center(self):
		cc_list = [
			{
				"cost_center_name": self.name,
				"company": self.name,
				"is_group": 1,
				"parent_cost_center": None,
			},
			{
				"cost_center_name": _("Main"),
				"company": self.name,
				"is_group": 0,
				"parent_cost_center": self.name + " - " + self.abbr,
			},
		]
		for cc in cc_list:
			cc.update({"doctype": "Cost Center"})
			cc_doc = finergy.get_doc(cc)
			cc_doc.flags.ignore_permissions = True

			if cc.get("cost_center_name") == self.name:
				cc_doc.flags.ignore_mandatory = True
			cc_doc.insert()

		finergy.db.set(self, "cost_center", _("Main") + " - " + self.abbr)
		finergy.db.set(self, "round_off_cost_center", _("Main") + " - " + self.abbr)
		finergy.db.set(self, "depreciation_cost_center", _("Main") + " - " + self.abbr)

	def after_rename(self, olddn, newdn, merge=False):
		finergy.db.set(self, "company_name", newdn)

		finergy.db.sql(
			"""update `tabDefaultValue` set defvalue=%s
			where defkey='Company' and defvalue=%s""",
			(newdn, olddn),
		)

		clear_defaults_cache()

	def abbreviate(self):
		self.abbr = "".join(c[0].upper() for c in self.company_name.split())

	def on_trash(self):
		"""
		Trash accounts and cost centers for this company if no gl entry exists
		"""
		NestedSet.validate_if_child_exists(self)
		finergy.utils.nestedset.update_nsm(self)

		rec = finergy.db.sql("SELECT name from `tabGL Entry` where company = %s", self.name)
		if not rec:
			finergy.db.sql(
				"""delete from `tabBudget Account`
				where exists(select name from tabBudget
					where name=`tabBudget Account`.parent and company = %s)""",
				self.name,
			)

			for doctype in ["Account", "Cost Center", "Budget", "Party Account"]:
				finergy.db.sql("delete from `tab{0}` where company = %s".format(doctype), self.name)

		if not finergy.db.get_value("Stock Ledger Entry", {"company": self.name}):
			finergy.db.sql("""delete from `tabWarehouse` where company=%s""", self.name)

		finergy.defaults.clear_default("company", value=self.name)
		for doctype in ["Mode of Payment Account", "Item Default"]:
			finergy.db.sql("delete from `tab{0}` where company = %s".format(doctype), self.name)

		# clear default accounts, warehouses from item
		warehouses = finergy.db.sql_list("select name from tabWarehouse where company=%s", self.name)
		if warehouses:
			finergy.db.sql(
				"""delete from `tabItem Reorder` where warehouse in (%s)"""
				% ", ".join(["%s"] * len(warehouses)),
				tuple(warehouses),
			)

		# reset default company
		finergy.db.sql(
			"""update `tabSingles` set value=""
			where doctype='Global Defaults' and field='default_company'
			and value=%s""",
			self.name,
		)

		# reset default company
		finergy.db.sql(
			"""update `tabSingles` set value=""
			where doctype='Chart of Accounts Importer' and field='company'
			and value=%s""",
			self.name,
		)

		# delete BOMs
		boms = finergy.db.sql_list("select name from tabBOM where company=%s", self.name)
		if boms:
			finergy.db.sql("delete from tabBOM where company=%s", self.name)
			for dt in ("BOM Operation", "BOM Item", "BOM Scrap Item", "BOM Explosion Item"):
				finergy.db.sql(
					"delete from `tab%s` where parent in (%s)" "" % (dt, ", ".join(["%s"] * len(boms))),
					tuple(boms),
				)

		finergy.db.sql("delete from tabEmployee where company=%s", self.name)
		finergy.db.sql("delete from tabDepartment where company=%s", self.name)
		finergy.db.sql("delete from `tabTax Withholding Account` where company=%s", self.name)
		finergy.db.sql("delete from `tabTransaction Deletion Record` where company=%s", self.name)

		# delete tax templates
		finergy.db.sql("delete from `tabSales Taxes and Charges Template` where company=%s", self.name)
		finergy.db.sql("delete from `tabPurchase Taxes and Charges Template` where company=%s", self.name)
		finergy.db.sql("delete from `tabItem Tax Template` where company=%s", self.name)

		# delete Process Deferred Accounts if no GL Entry found
		if not finergy.db.get_value("GL Entry", {"company": self.name}):
			finergy.db.sql("delete from `tabProcess Deferred Accounting` where company=%s", self.name)

	def check_parent_changed(self):
		finergy.flags.parent_company_changed = False

		if not self.is_new() and self.parent_company != finergy.db.get_value(
			"Company", self.name, "parent_company"
		):
			finergy.flags.parent_company_changed = True


def get_name_with_abbr(name, company):
	company_abbr = finergy.get_cached_value("Company", company, "abbr")
	parts = name.split(" - ")

	if parts[-1].lower() != company_abbr.lower():
		parts.append(company_abbr)

	return " - ".join(parts)


def install_country_fixtures(company, country):
	path = finergy.get_app_path("capkpi", "regional", finergy.scrub(country))
	if os.path.exists(path.encode("utf-8")):
		try:
			module_name = "capkpi.regional.{0}.setup.setup".format(finergy.scrub(country))
			finergy.get_attr(module_name)(company, False)
		except Exception as e:
			finergy.log_error()
			finergy.throw(
				_("Failed to setup defaults for country {0}. Please contact support@capkpi.com").format(
					finergy.bold(country)
				)
			)


def update_company_current_month_sales(company):
	current_month_year = formatdate(today(), "MM-yyyy")

	results = finergy.db.sql(
		"""
		SELECT
			SUM(base_grand_total) AS total,
			DATE_FORMAT(`posting_date`, '%m-%Y') AS month_year
		FROM
			`tabSales Invoice`
		WHERE
			DATE_FORMAT(`posting_date`, '%m-%Y') = '{current_month_year}'
			AND docstatus = 1
			AND company = {company}
		GROUP BY
			month_year
	""".format(
			current_month_year=current_month_year, company=finergy.db.escape(company)
		),
		as_dict=True,
	)

	monthly_total = results[0]["total"] if len(results) > 0 else 0

	finergy.db.set_value("Company", company, "total_monthly_sales", monthly_total)


def update_company_monthly_sales(company):
	"""Cache past year monthly sales of every company based on sales invoices"""
	import json

	from finergy.utils.goal import get_monthly_results

	filter_str = "company = {0} and status != 'Draft' and docstatus=1".format(
		finergy.db.escape(company)
	)
	month_to_value_dict = get_monthly_results(
		"Sales Invoice", "base_grand_total", "posting_date", filter_str, "sum"
	)

	finergy.db.set_value("Company", company, "sales_monthly_history", json.dumps(month_to_value_dict))


def update_transactions_annual_history(company, commit=False):
	transactions_history = get_all_transactions_annual_history(company)
	finergy.db.set_value(
		"Company", company, "transactions_annual_history", json.dumps(transactions_history)
	)

	if commit:
		finergy.db.commit()


def cache_companies_monthly_sales_history():
	companies = [d["name"] for d in finergy.get_list("Company")]
	for company in companies:
		update_company_monthly_sales(company)
		update_transactions_annual_history(company)
	finergy.db.commit()


@finergy.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False):
	if parent == None or parent == "All Companies":
		parent = ""

	return finergy.db.sql(
		"""
		select
			name as value,
			is_group as expandable
		from
			`tab{doctype}` comp
		where
			ifnull(parent_company, "")={parent}
		""".format(
			doctype=doctype, parent=finergy.db.escape(parent)
		),
		as_dict=1,
	)


@finergy.whitelist()
def add_node():
	from finergy.desk.treeview import make_tree_args

	args = finergy.form_dict
	args = make_tree_args(**args)

	if args.parent_company == "All Companies":
		args.parent_company = None

	finergy.get_doc(args).insert()


def get_all_transactions_annual_history(company):
	out = {}

	items = finergy.db.sql(
		"""
		select transaction_date, count(*) as count

		from (
			select name, transaction_date, company
			from `tabQuotation`

			UNION ALL

			select name, transaction_date, company
			from `tabSales Order`

			UNION ALL

			select name, posting_date as transaction_date, company
			from `tabDelivery Note`

			UNION ALL

			select name, posting_date as transaction_date, company
			from `tabSales Invoice`

			UNION ALL

			select name, creation as transaction_date, company
			from `tabIssue`

			UNION ALL

			select name, creation as transaction_date, company
			from `tabProject`
		) t

		where
			company=%s
			and
			transaction_date > date_sub(curdate(), interval 1 year)

		group by
			transaction_date
			""",
		(company),
		as_dict=True,
	)

	for d in items:
		timestamp = get_timestamp(d["transaction_date"])
		out.update({timestamp: d["count"]})

	return out


def get_timeline_data(doctype, name):
	"""returns timeline data based on linked records in dashboard"""
	out = {}
	date_to_value_dict = {}

	history = finergy.get_cached_value("Company", name, "transactions_annual_history")

	try:
		date_to_value_dict = json.loads(history) if history and "{" in history else None
	except ValueError:
		date_to_value_dict = None

	if date_to_value_dict is None:
		update_transactions_annual_history(name, True)
		history = finergy.get_cached_value("Company", name, "transactions_annual_history")
		return json.loads(history) if history and "{" in history else {}

	return date_to_value_dict


@finergy.whitelist()
def get_default_company_address(name, sort_key="is_primary_address", existing_address=None):
	if sort_key not in ["is_shipping_address", "is_primary_address"]:
		return None

	out = finergy.db.sql(
		""" SELECT
			addr.name, addr.%s
		FROM
			`tabAddress` addr, `tabDynamic Link` dl
		WHERE
			dl.parent = addr.name and dl.link_doctype = 'Company' and
			dl.link_name = %s and ifnull(addr.disabled, 0) = 0
		"""
		% (sort_key, "%s"),
		(name),
	)  # nosec

	if existing_address:
		if existing_address in [d[0] for d in out]:
			return existing_address

	if out:
		return sorted(out, key=functools.cmp_to_key(lambda x, y: cmp(y[1], x[1])))[0][0]
	else:
		return None


@finergy.whitelist()
def create_transaction_deletion_request(company):
	tdr = finergy.get_doc({"doctype": "Transaction Deletion Record", "company": company})
	tdr.insert()
	tdr.submit()
