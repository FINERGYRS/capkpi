import finergy


def execute():
	finergy.reload_doc("hr", "doctype", "training_event")
	finergy.reload_doc("hr", "doctype", "training_event_employee")

	finergy.db.sql("update `tabTraining Event Employee` set `attendance` = 'Present'")
	finergy.db.sql(
		"update `tabTraining Event Employee` set `is_mandatory` = 1 where `attendance` = 'Mandatory'"
	)
