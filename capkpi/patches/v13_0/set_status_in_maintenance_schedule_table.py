import finergy


def execute():
	finergy.reload_doc("maintenance", "doctype", "Maintenance Schedule Detail")
	finergy.db.sql(
		"""
		UPDATE `tabMaintenance Schedule Detail`
		SET completion_status = 'Pending'
		WHERE docstatus < 2
	"""
	)
