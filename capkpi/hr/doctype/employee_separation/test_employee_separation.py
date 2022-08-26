# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy

test_dependencies = ["Employee Onboarding"]


class TestEmployeeSeparation(unittest.TestCase):
	def test_employee_separation(self):
		employee = finergy.db.get_value("Employee", {"status": "Active"})
		separation = finergy.new_doc("Employee Separation")
		separation.employee = employee
		separation.company = "_Test Company"
		separation.append("activities", {"activity_name": "Deactivate Employee", "role": "HR User"})
		separation.boarding_status = "Pending"
		separation.insert()
		separation.submit()
		self.assertEqual(separation.docstatus, 1)
		separation.cancel()
		self.assertEqual(separation.project, "")
