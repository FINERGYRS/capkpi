import click
import finergy


def execute():

	finergy.reload_doc("capkpi_integrations", "doctype", "amazon_mws_settings")
	if not finergy.db.get_single_value("Amazon MWS Settings", "enable_amazon"):
		return

	click.secho(
		"Amazon MWS Integration is moved to a separate app and will be removed from CapKPI in version-14.\n"
		"Please install the app to continue using the integration: https://github.com/finergyrs/ecommerce_integrations",
		fg="yellow",
	)
