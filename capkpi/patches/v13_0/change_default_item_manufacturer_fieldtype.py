import finergy


def execute():

	# Erase all default item manufacturers that dont exist.
	item = finergy.qb.DocType("Item")
	manufacturer = finergy.qb.DocType("Manufacturer")

	(
		finergy.qb.update(item)
		.set(item.default_item_manufacturer, None)
		.left_join(manufacturer)
		.on(item.default_item_manufacturer == manufacturer.name)
		.where(manufacturer.name.isnull() & item.default_item_manufacturer.isnotnull())
	).run()
