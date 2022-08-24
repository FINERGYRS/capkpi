import finergy


def execute():
	from capkpi.setup.setup_wizard.operations.install_fixtures import add_uom_data

	finergy.reload_doc("setup", "doctype", "UOM Conversion Factor")
	finergy.reload_doc("setup", "doctype", "UOM")
	finergy.reload_doc("stock", "doctype", "UOM Category")

	add_uom_data()
