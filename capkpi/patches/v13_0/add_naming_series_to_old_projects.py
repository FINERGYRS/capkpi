import finergy


def execute():
	finergy.reload_doc("projects", "doctype", "project")

	finergy.db.sql(
		"""UPDATE `tabProject`
		SET
			naming_series = 'PROJ-.####'
		WHERE
			naming_series is NULL"""
	)
