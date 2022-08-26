import finergy
from finergy.installer import remove_from_installed_apps


def execute():
	finergy.reload_doc("capkpi_integrations", "doctype", "shopify_settings")
	finergy.reload_doc("capkpi_integrations", "doctype", "shopify_tax_account")
	finergy.reload_doc("capkpi_integrations", "doctype", "shopify_log")
	finergy.reload_doc("capkpi_integrations", "doctype", "shopify_webhook_detail")

	if "capkpi_shopify" in finergy.get_installed_apps():
		remove_from_installed_apps("capkpi_shopify")

		finergy.delete_doc("Module Def", "capkpi_shopify")

		finergy.db.commit()

		finergy.db.sql("truncate `tabShopify Log`")

		setup_app_type()
	else:
		disable_shopify()


def setup_app_type():
	try:
		shopify_settings = finergy.get_doc("Shopify Settings")
		shopify_settings.app_type = "Private"
		shopify_settings.update_price_in_capkpi_price_list = (
			0 if getattr(shopify_settings, "push_prices_to_shopify", None) else 1
		)
		shopify_settings.flags.ignore_mandatory = True
		shopify_settings.ignore_permissions = True
		shopify_settings.save()
	except Exception:
		finergy.db.set_value("Shopify Settings", None, "enable_shopify", 0)
		finergy.log_error(finergy.get_traceback())


def disable_shopify():
	# due to finergy.db.set_value wrongly written and enable_shopify being default 1
	# Shopify Settings isn't properly configured and leads to error
	shopify = finergy.get_doc("Shopify Settings")

	if (
		shopify.app_type == "Public"
		or shopify.app_type == None
		or (shopify.enable_shopify and not (shopify.shopify_url or shopify.api_key))
	):
		finergy.db.set_value("Shopify Settings", None, "enable_shopify", 0)
