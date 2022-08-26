import finergy


def execute():
	if not finergy.db.table_exists("Additional Salary"):
		return

	for doctype in ("Additional Salary", "Employee Incentive", "Salary Detail"):
		finergy.reload_doc("Payroll", "doctype", doctype)

	finergy.reload_doc("hr", "doctype", "Leave Encashment")

	if finergy.db.has_column("Leave Encashment", "additional_salary"):
		leave_encashments = finergy.get_all(
			"Leave Encashment",
			fields=["name", "additional_salary"],
			filters={"additional_salary": ["!=", ""]},
		)
		for leave_encashment in leave_encashments:
			finergy.db.sql(
				""" UPDATE `tabAdditional Salary`
				SET ref_doctype = 'Leave Encashment', ref_docname = %s
				WHERE name = %s
			""",
				(leave_encashment["name"], leave_encashment["additional_salary"]),
			)

	if finergy.db.has_column("Employee Incentive", "additional_salary"):
		employee_incentives = finergy.get_all(
			"Employee Incentive",
			fields=["name", "additional_salary"],
			filters={"additional_salary": ["!=", ""]},
		)

		for incentive in employee_incentives:
			finergy.db.sql(
				""" UPDATE `tabAdditional Salary`
				SET ref_doctype = 'Employee Incentive', ref_docname = %s
				WHERE name = %s
			""",
				(incentive["name"], incentive["additional_salary"]),
			)

	if finergy.db.has_column("Additional Salary", "salary_slip"):
		additional_salaries = finergy.get_all(
			"Additional Salary",
			fields=["name", "salary_slip", "type", "salary_component"],
			filters={"salary_slip": ["!=", ""]},
			group_by="salary_slip",
		)

		salary_slips = [sal["salary_slip"] for sal in additional_salaries]

		for salary in additional_salaries:
			comp_type = "earnings" if salary["type"] == "Earning" else "deductions"
			if salary["salary_slip"] and salary_slips.count(salary["salary_slip"]) == 1:
				finergy.db.sql(
					"""
					UPDATE `tabSalary Detail`
					SET additional_salary = %s
					WHERE parenttype = 'Salary Slip'
						and parentfield = %s
						and parent = %s
						and salary_component = %s
				""",
					(salary["name"], comp_type, salary["salary_slip"], salary["salary_component"]),
				)
