import finergy


def execute():
	from capkpi.setup.setup_wizard.operations.install_fixtures import add_uom_data

	finergy.reload_doc("setup", "doctype", "UOM Conversion Factor")
	finergy.reload_doc("setup", "doctype", "UOM")
	finergy.reload_doc("stock", "doctype", "UOM Category")

	if not finergy.db.a_row_exists("UOM Conversion Factor"):
		add_uom_data()
	else:
		# delete conversion data and insert again
		finergy.db.sql("delete from `tabUOM Conversion Factor`")
		try:
			finergy.delete_doc("UOM", "Hundredweight")
			finergy.delete_doc("UOM", "Pound Cubic Yard")
		except finergy.LinkExistsError:
			pass

		add_uom_data()
