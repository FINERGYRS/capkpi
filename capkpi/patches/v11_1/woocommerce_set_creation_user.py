import finergy
from finergy.utils import cint


def execute():
	finergy.reload_doc("capkpi_integrations", "doctype", "woocommerce_settings")
	doc = finergy.get_doc("Woocommerce Settings")

	if cint(doc.enable_sync):
		doc.creation_user = doc.modified_by
		doc.save(ignore_permissions=True)
