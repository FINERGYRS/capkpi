import finergy


def execute():
	finergy.reload_doc("hub_node", "doctype", "Marketplace Settings")
	finergy.db.set_value(
		"Marketplace Settings", "Marketplace Settings", "marketplace_url", "https://hubmarket.org"
	)
