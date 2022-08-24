import finergy


def execute():
	finergy.reload_doc("accounts", "doctype", "pos_closing_entry")

	finergy.db.sql("update `tabPOS Closing Entry` set `status` = 'Failed' where `status` = 'Queued'")
