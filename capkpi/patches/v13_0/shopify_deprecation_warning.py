import click
import finergy


def execute():

	finergy.reload_doc("capkpi_integrations", "doctype", "shopify_settings")
	if not finergy.db.get_single_value("Shopify Settings", "enable_shopify"):
		return

	click.secho(
		"Shopify Integration is moved to a separate app and will be removed from CapKPI in version-14.\n"
		"Please install the app to continue using the integration: https://github.com/finergyrs/ecommerce_integrations",
		fg="yellow",
	)
