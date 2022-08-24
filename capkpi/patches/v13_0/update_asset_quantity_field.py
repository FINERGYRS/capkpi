import finergy


def execute():
	if finergy.db.count("Asset"):
		finergy.reload_doc("assets", "doctype", "Asset")
		asset = finergy.qb.DocType("Asset")
		finergy.qb.update(asset).set(asset.asset_quantity, 1).run()
