# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class ExpenseClaimType(Document):
	def validate(self):
		self.validate_accounts()
		self.validate_repeating_companies()

	def validate_repeating_companies(self):
		"""Error when Same Company is entered multiple times in accounts"""
		accounts_list = []
		for entry in self.accounts:
			accounts_list.append(entry.company)

		if len(accounts_list) != len(set(accounts_list)):
			finergy.throw(_("Same Company is entered more than once"))

	def validate_accounts(self):
		for entry in self.accounts:
			"""Error when Company of Ledger account doesn't match with Company Selected"""
			if finergy.db.get_value("Account", entry.default_account, "company") != entry.company:
				finergy.throw(
					_("Account {0} does not match with Company {1}").format(entry.default_account, entry.company)
				)
