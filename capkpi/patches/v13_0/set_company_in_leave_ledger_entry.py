import finergy


def execute():
	finergy.reload_doc("HR", "doctype", "Leave Allocation")
	finergy.reload_doc("HR", "doctype", "Leave Ledger Entry")
	finergy.db.sql(
		"""update `tabLeave Ledger Entry` as lle set company = (select company from `tabEmployee` where employee = lle.employee)"""
	)
	finergy.db.sql(
		"""update `tabLeave Allocation` as la set company = (select company from `tabEmployee` where employee = la.employee)"""
	)
