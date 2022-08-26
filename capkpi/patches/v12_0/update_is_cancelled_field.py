import finergy


def execute():
	# handle type casting for is_cancelled field
	module_doctypes = (
		("stock", "Stock Ledger Entry"),
		("stock", "Serial No"),
		("accounts", "GL Entry"),
	)

	for module, doctype in module_doctypes:
		if (
			not finergy.db.has_column(doctype, "is_cancelled")
			or finergy.db.get_column_type(doctype, "is_cancelled").lower() == "int(1)"
		):
			continue

		finergy.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 0
				where is_cancelled in ('', 'No') or is_cancelled is NULL""".format(
				doctype=doctype
			)
		)
		finergy.db.sql(
			"""
				UPDATE `tab{doctype}`
				SET is_cancelled = 1
				where is_cancelled = 'Yes'""".format(
				doctype=doctype
			)
		)

		finergy.reload_doc(module, "doctype", finergy.scrub(doctype))
