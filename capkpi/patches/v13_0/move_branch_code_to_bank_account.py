# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():

	finergy.reload_doc("accounts", "doctype", "bank_account")
	finergy.reload_doc("accounts", "doctype", "bank")

	if finergy.db.has_column("Bank", "branch_code") and finergy.db.has_column(
		"Bank Account", "branch_code"
	):
		finergy.db.sql(
			"""UPDATE `tabBank` b, `tabBank Account` ba
			SET ba.branch_code = b.branch_code
			WHERE ba.bank = b.name AND
			ifnull(b.branch_code, '') != '' AND ifnull(ba.branch_code, '') = ''"""
		)
