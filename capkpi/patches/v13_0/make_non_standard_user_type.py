# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from six import iteritems

from capkpi.setup.install import add_non_standard_user_types


def execute():
	doctype_dict = {
		"projects": ["Timesheet"],
		"payroll": [
			"Salary Slip",
			"Employee Tax Exemption Declaration",
			"Employee Tax Exemption Proof Submission",
		],
		"hr": [
			"Employee",
			"Expense Claim",
			"Leave Application",
			"Attendance Request",
			"Compensatory Leave Request",
		],
	}

	for module, doctypes in iteritems(doctype_dict):
		for doctype in doctypes:
			finergy.reload_doc(module, "doctype", doctype)

	finergy.flags.ignore_select_perm = True
	finergy.flags.update_select_perm_after_migrate = True

	add_non_standard_user_types()
