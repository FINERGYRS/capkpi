import finergy


def execute():
	finergy.reload_doc("accounts", "doctype", "accounts_settings")

	finergy.db.set_value(
		"Accounts Settings", None, "automatically_process_deferred_accounting_entry", 1
	)
