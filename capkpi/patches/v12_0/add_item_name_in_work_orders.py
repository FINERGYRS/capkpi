import finergy


def execute():
	finergy.reload_doc("manufacturing", "doctype", "work_order")

	finergy.db.sql(
		"""
		UPDATE
			`tabWork Order` wo
				JOIN `tabItem` item ON wo.production_item = item.item_code
		SET
			wo.item_name = item.item_name
	"""
	)
	finergy.db.commit()
