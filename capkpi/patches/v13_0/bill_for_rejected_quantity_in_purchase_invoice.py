import finergy


def execute():
	finergy.reload_doctype("Buying Settings")
	buying_settings = finergy.get_single("Buying Settings")
	buying_settings.bill_for_rejected_quantity_in_purchase_invoice = 0
	buying_settings.save()
