import finergy


def execute():
	finergy.delete_doc("DocType", "Shopify Settings", ignore_missing=True)
	finergy.delete_doc("DocType", "Shopify Log", ignore_missing=True)
