import finergy


def execute():
	"""Correct amount in child table of required items table."""

	finergy.reload_doc("manufacturing", "doctype", "work_order")
	finergy.reload_doc("manufacturing", "doctype", "work_order_item")

	finergy.db.sql("""UPDATE `tabWork Order Item` SET amount = rate * required_qty""")
