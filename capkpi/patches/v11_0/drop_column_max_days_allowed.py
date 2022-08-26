import finergy


def execute():
	if finergy.db.exists("DocType", "Leave Type"):
		if "max_days_allowed" in finergy.db.get_table_columns("Leave Type"):
			finergy.db.sql("alter table `tabLeave Type` drop column max_days_allowed")
