# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors and contributors
# For license information, please see license.txt


import finergy


@finergy.whitelist()
def enable_hub():
	hub_settings = finergy.get_doc("Marketplace Settings")
	hub_settings.register()
	finergy.db.commit()
	return hub_settings


@finergy.whitelist()
def sync():
	hub_settings = finergy.get_doc("Marketplace Settings")
	hub_settings.sync()
