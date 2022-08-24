# Copyright (c) 2018, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	if finergy.db.table_exists("Bank Reconciliation"):
		finergy.rename_doc("DocType", "Bank Reconciliation", "Bank Clearance", force=True)
		finergy.reload_doc("Accounts", "doctype", "Bank Clearance")

		finergy.rename_doc("DocType", "Bank Reconciliation Detail", "Bank Clearance Detail", force=True)
		finergy.reload_doc("Accounts", "doctype", "Bank Clearance Detail")
