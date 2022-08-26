import finergy


def execute():
	finergy.reload_doc("capkpi_integrations", "doctype", "shopify_settings")
	finergy.db.set_value("Shopify Settings", None, "app_type", "Private")
