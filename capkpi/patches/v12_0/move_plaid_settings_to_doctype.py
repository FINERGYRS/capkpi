# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("capkpi_integrations", "doctype", "plaid_settings")
	plaid_settings = finergy.get_single("Plaid Settings")
	if plaid_settings.enabled:
		if not (finergy.conf.plaid_client_id and finergy.conf.plaid_env and finergy.conf.plaid_secret):
			plaid_settings.enabled = 0
		else:
			plaid_settings.update(
				{
					"plaid_client_id": finergy.conf.plaid_client_id,
					"plaid_env": finergy.conf.plaid_env,
					"plaid_secret": finergy.conf.plaid_secret,
				}
			)
		plaid_settings.flags.ignore_mandatory = True
		plaid_settings.save()
