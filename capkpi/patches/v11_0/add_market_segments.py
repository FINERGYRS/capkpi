import finergy

from capkpi.setup.setup_wizard.operations.install_fixtures import add_market_segments


def execute():
	finergy.reload_doc("crm", "doctype", "market_segment")

	finergy.local.lang = finergy.db.get_default("lang") or "en"

	add_market_segments()
