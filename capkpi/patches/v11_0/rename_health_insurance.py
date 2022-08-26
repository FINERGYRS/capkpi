# Copyright (c) 2018, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.rename_doc("DocType", "Health Insurance", "Employee Health Insurance", force=True)
	finergy.reload_doc("hr", "doctype", "employee_health_insurance")
