# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	if finergy.db.table_exists("Asset Adjustment") and not finergy.db.table_exists(
		"Asset Value Adjustment"
	):
		finergy.rename_doc("DocType", "Asset Adjustment", "Asset Value Adjustment", force=True)
		finergy.reload_doc("assets", "doctype", "asset_value_adjustment")
