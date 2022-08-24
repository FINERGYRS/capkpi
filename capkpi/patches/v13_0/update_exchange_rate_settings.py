import finergy

from capkpi.setup.install import setup_currency_exchange


def execute():
	finergy.reload_doc("accounts", "doctype", "currency_exchange_settings_result")
	finergy.reload_doc("accounts", "doctype", "currency_exchange_settings_details")
	finergy.reload_doc("accounts", "doctype", "currency_exchange_settings")
	setup_currency_exchange()
