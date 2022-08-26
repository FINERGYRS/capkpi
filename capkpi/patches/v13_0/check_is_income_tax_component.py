# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.custom.doctype.custom_field.custom_field import create_custom_field

import capkpi


def execute():

	doctypes = [
		"salary_component",
		"Employee Tax Exemption Declaration",
		"Employee Tax Exemption Proof Submission",
		"Employee Tax Exemption Declaration Category",
		"Employee Tax Exemption Proof Submission Detail",
		"gratuity_rule",
		"gratuity_rule_slab",
		"gratuity_applicable_component",
	]

	for doctype in doctypes:
		finergy.reload_doc("Payroll", "doctype", doctype, force=True)

	reports = ["Professional Tax Deductions", "Provident Fund Deductions", "E-Invoice Summary"]
	for report in reports:
		finergy.reload_doc("Regional", "Report", report)
		finergy.reload_doc("Regional", "Report", report)

	if capkpi.get_region() == "India":
		create_custom_field(
			"Salary Component",
			dict(
				fieldname="component_type",
				label="Component Type",
				fieldtype="Select",
				insert_after="description",
				options="\nProvident Fund\nAdditional Provident Fund\nProvident Fund Loan\nProfessional Tax",
				depends_on='eval:doc.type == "Deduction"',
			),
		)

	if finergy.db.exists("Salary Component", "Income Tax"):
		finergy.db.set_value("Salary Component", "Income Tax", "is_income_tax_component", 1)
	if finergy.db.exists("Salary Component", "TDS"):
		finergy.db.set_value("Salary Component", "TDS", "is_income_tax_component", 1)

	components = finergy.db.sql(
		"select name from `tabSalary Component` where variable_based_on_taxable_salary = 1", as_dict=1
	)
	for component in components:
		finergy.db.set_value("Salary Component", component.name, "is_income_tax_component", 1)

	if capkpi.get_region() == "India":
		if finergy.db.exists("Salary Component", "Provident Fund"):
			finergy.db.set_value("Salary Component", "Provident Fund", "component_type", "Provident Fund")
		if finergy.db.exists("Salary Component", "Professional Tax"):
			finergy.db.set_value(
				"Salary Component", "Professional Tax", "component_type", "Professional Tax"
			)
