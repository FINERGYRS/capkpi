# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

import unittest

import finergy
import finergy.utils

import capkpi
from capkpi.hr.doctype.employee.employee import InactiveEmployeeStatusError

test_records = finergy.get_test_records("Employee")


class TestEmployee(unittest.TestCase):
	def test_employee_status_left(self):
		employee1 = make_employee("test_employee_1@company.com")
		employee2 = make_employee("test_employee_2@company.com")
		employee1_doc = finergy.get_doc("Employee", employee1)
		employee2_doc = finergy.get_doc("Employee", employee2)
		employee2_doc.reload()
		employee2_doc.reports_to = employee1_doc.name
		employee2_doc.save()
		employee1_doc.reload()
		employee1_doc.status = "Left"
		self.assertRaises(InactiveEmployeeStatusError, employee1_doc.save)

	def test_employee_status_inactive(self):
		from capkpi.payroll.doctype.salary_slip.test_salary_slip import make_holiday_list
		from capkpi.payroll.doctype.salary_structure.salary_structure import make_salary_slip
		from capkpi.payroll.doctype.salary_structure.test_salary_structure import make_salary_structure

		employee = make_employee("test_employee_status@company.com")
		employee_doc = finergy.get_doc("Employee", employee)
		employee_doc.status = "Inactive"
		employee_doc.save()
		employee_doc.reload()

		make_holiday_list()
		finergy.db.set_value(
			"Company", employee_doc.company, "default_holiday_list", "Salary Slip Test Holiday List"
		)

		finergy.db.sql(
			"""delete from `tabSalary Structure` where name='Test Inactive Employee Salary Slip'"""
		)
		salary_structure = make_salary_structure(
			"Test Inactive Employee Salary Slip",
			"Monthly",
			employee=employee_doc.name,
			company=employee_doc.company,
		)
		salary_slip = make_salary_slip(salary_structure.name, employee=employee_doc.name)

		self.assertRaises(InactiveEmployeeStatusError, salary_slip.save)

	def tearDown(self):
		finergy.db.rollback()


def make_employee(user, company=None, **kwargs):
	if not finergy.db.get_value("User", user):
		finergy.get_doc(
			{
				"doctype": "User",
				"email": user,
				"first_name": user,
				"new_password": "password",
				"send_welcome_email": 0,
				"roles": [{"doctype": "Has Role", "role": "Employee"}],
			}
		).insert()

	if not finergy.db.get_value("Employee", {"user_id": user}):
		employee = finergy.get_doc(
			{
				"doctype": "Employee",
				"naming_series": "EMP-",
				"first_name": user,
				"company": company or capkpi.get_default_company(),
				"user_id": user,
				"date_of_birth": "1990-05-08",
				"date_of_joining": "2013-01-01",
				"department": finergy.get_all("Department", fields="name")[0].name,
				"gender": "Female",
				"company_email": user,
				"prefered_contact_email": "Company Email",
				"prefered_email": user,
				"status": "Active",
				"employment_type": "Intern",
			}
		)
		if kwargs:
			employee.update(kwargs)
		employee.insert()
		return employee.name
	else:
		finergy.db.set_value("Employee", {"employee_name": user}, "status", "Active")
		return finergy.get_value("Employee", {"employee_name": user}, "name")
