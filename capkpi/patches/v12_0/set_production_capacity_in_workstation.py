import finergy


def execute():
	finergy.reload_doc("manufacturing", "doctype", "workstation")

	finergy.db.sql(
		""" UPDATE `tabWorkstation`
        SET production_capacity = 1 """
	)
