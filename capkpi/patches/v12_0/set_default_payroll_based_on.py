import finergy


def execute():
	finergy.reload_doc("hr", "doctype", "hr_settings")
	finergy.db.set_value("HR Settings", None, "payroll_based_on", "Leave")
