import finergy


def execute():
	finergy.reload_doc("Payroll", "doctype", "salary_detail")
	finergy.reload_doc("Payroll", "doctype", "salary_component")

	finergy.db.sql("update `tabSalary Component` set is_tax_applicable=1 where type='Earning'")

	finergy.db.sql(
		"""update `tabSalary Component` set variable_based_on_taxable_salary=1
	    where type='Deduction' and name in ('TDS', 'Tax Deducted at Source')"""
	)

	finergy.db.sql(
		"""update `tabSalary Detail` set is_tax_applicable=1
	    where parentfield='earnings' and statistical_component=0"""
	)
	finergy.db.sql(
		"""update `tabSalary Detail` set variable_based_on_taxable_salary=1
	    where parentfield='deductions' and salary_component in ('TDS', 'Tax Deducted at Source')"""
	)
