# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("manufacturing", "doctype", "job_card")
	finergy.reload_doc("manufacturing", "doctype", "job_card_item")
	finergy.reload_doc("manufacturing", "doctype", "work_order_operation")

	finergy.db.sql(
		""" update `tabJob Card` jc, `tabWork Order Operation` wo
		SET	jc.hour_rate =  wo.hour_rate
		WHERE
			jc.operation_id = wo.name and jc.docstatus < 2 and wo.hour_rate > 0
	"""
	)
