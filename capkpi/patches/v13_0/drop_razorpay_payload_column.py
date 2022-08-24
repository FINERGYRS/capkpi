import finergy


def execute():
	if finergy.db.exists("DocType", "Membership"):
		if "webhook_payload" in finergy.db.get_table_columns("Membership"):
			finergy.db.sql("alter table `tabMembership` drop column webhook_payload")
