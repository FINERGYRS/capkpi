# Copyright (c) 2017, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

from capkpi.manufacturing.doctype.work_order.work_order import create_job_card


def execute():
	finergy.reload_doc("manufacturing", "doctype", "work_order")
	finergy.reload_doc("manufacturing", "doctype", "work_order_item")
	finergy.reload_doc("manufacturing", "doctype", "job_card")
	finergy.reload_doc("manufacturing", "doctype", "job_card_item")

	fieldname = finergy.db.get_value(
		"DocField", {"fieldname": "work_order", "parent": "Timesheet"}, "fieldname"
	)
	if not fieldname:
		fieldname = finergy.db.get_value(
			"DocField", {"fieldname": "production_order", "parent": "Timesheet"}, "fieldname"
		)
		if not fieldname:
			return

	for d in finergy.get_all(
		"Timesheet", filters={fieldname: ["!=", ""], "docstatus": 0}, fields=[fieldname, "name"]
	):
		if d[fieldname]:
			doc = finergy.get_doc("Work Order", d[fieldname])
			for row in doc.operations:
				create_job_card(doc, row, auto_create=True)
			finergy.delete_doc("Timesheet", d.name)
