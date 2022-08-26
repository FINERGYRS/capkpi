import finergy


def execute():
	finergy.reload_doc("manufacturing", "doctype", "bom_operation")
	finergy.reload_doc("manufacturing", "doctype", "work_order_operation")

	finergy.db.sql(
		"""
        UPDATE
            `tabBOM Operation` bo
        SET
            bo.batch_size = 1
    """
	)
	finergy.db.sql(
		"""
        UPDATE
            `tabWork Order Operation` wop
        SET
            wop.batch_size = 1
    """
	)
