import finergy

# this patch should have been included with this PR https://github.com/finergyrs/capkpi/pull/14302


def execute():
	if finergy.db.table_exists("Additional Salary Component"):
		if not finergy.db.table_exists("Additional Salary"):
			finergy.rename_doc("DocType", "Additional Salary Component", "Additional Salary")

		finergy.delete_doc("DocType", "Additional Salary Component")
