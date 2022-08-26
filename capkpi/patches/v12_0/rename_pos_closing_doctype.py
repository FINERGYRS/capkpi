# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	if finergy.db.table_exists("POS Closing Voucher"):
		if not finergy.db.exists("DocType", "POS Closing Entry"):
			finergy.rename_doc("DocType", "POS Closing Voucher", "POS Closing Entry", force=True)

		if not finergy.db.exists("DocType", "POS Closing Entry Taxes"):
			finergy.rename_doc("DocType", "POS Closing Voucher Taxes", "POS Closing Entry Taxes", force=True)

		if not finergy.db.exists("DocType", "POS Closing Voucher Details"):
			finergy.rename_doc(
				"DocType", "POS Closing Voucher Details", "POS Closing Entry Detail", force=True
			)

		finergy.reload_doc("Accounts", "doctype", "POS Closing Entry")
		finergy.reload_doc("Accounts", "doctype", "POS Closing Entry Taxes")
		finergy.reload_doc("Accounts", "doctype", "POS Closing Entry Detail")

	if finergy.db.exists("DocType", "POS Closing Voucher"):
		finergy.delete_doc("DocType", "POS Closing Voucher")
		finergy.delete_doc("DocType", "POS Closing Voucher Taxes")
		finergy.delete_doc("DocType", "POS Closing Voucher Details")
		finergy.delete_doc("DocType", "POS Closing Voucher Invoices")
