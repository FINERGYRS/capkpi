import finergy


def execute():
	finergy.reload_doc("Hub Node", "doctype", "Hub Tracked Item")
	if not finergy.db.a_row_exists("Hub Tracked Item"):
		return

	finergy.db.sql(
		"""
		Update `tabHub Tracked Item`
		SET published = 1
	"""
	)
