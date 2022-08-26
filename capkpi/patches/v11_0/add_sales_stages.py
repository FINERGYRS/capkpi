import finergy

from capkpi.setup.setup_wizard.operations.install_fixtures import add_sale_stages


def execute():
	finergy.reload_doc("crm", "doctype", "sales_stage")

	finergy.local.lang = finergy.db.get_default("lang") or "en"

	add_sale_stages()
