import finergy

# Set department value based on employee value


def execute():

	doctypes_to_update = {
		"projects": ["Activity Cost", "Timesheet"],
		"setup": ["Sales Person"],
	}

	for module, doctypes in doctypes_to_update.items():
		for doctype in doctypes:
			if finergy.db.table_exists(doctype):
				finergy.reload_doc(module, "doctype", finergy.scrub(doctype))
				finergy.db.sql(
					"""
					update `tab%s` dt
					set department=(select department from `tabEmployee` where name=dt.employee)
				"""
					% doctype
				)
