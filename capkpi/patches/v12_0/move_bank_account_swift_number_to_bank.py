import finergy


def execute():
	finergy.reload_doc("accounts", "doctype", "bank", force=1)

	if (
		finergy.db.table_exists("Bank")
		and finergy.db.table_exists("Bank Account")
		and finergy.db.has_column("Bank Account", "swift_number")
	):
		try:
			finergy.db.sql(
				"""
				UPDATE `tabBank` b, `tabBank Account` ba
				SET b.swift_number = ba.swift_number WHERE b.name = ba.bank
			"""
			)
		except Exception as e:
			finergy.log_error("Bank to Bank Account patch migration failed")

	finergy.reload_doc("accounts", "doctype", "bank_account")
	finergy.reload_doc("accounts", "doctype", "payment_request")
