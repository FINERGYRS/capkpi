# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# MIT License. See license.txt


import finergy

from capkpi.capkpi_integrations.doctype.shopify_settings.shopify_settings import (
	setup_custom_fields,
)


def execute():
	if finergy.db.get_single_value("Shopify Settings", "enable_shopify"):
		setup_custom_fields()
