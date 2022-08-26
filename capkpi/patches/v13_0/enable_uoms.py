import finergy


def execute():
	finergy.reload_doc("setup", "doctype", "uom")

	uom = finergy.qb.DocType("UOM")

	(
		finergy.qb.update(uom)
		.set(uom.enabled, 1)
		.where(uom.creation >= "2021-10-18")  # date when this field was released
	).run()
