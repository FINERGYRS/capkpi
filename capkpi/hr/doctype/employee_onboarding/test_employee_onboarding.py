# Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
# See license.txt

import unittest

import finergy
from finergy.utils import nowdate

from capkpi.hr.doctype.employee_onboarding.employee_onboarding import (
	IncompleteTaskError,
	make_employee,
)
from capkpi.hr.doctype.job_offer.test_job_offer import create_job_offer


class TestEmployeeOnboarding(unittest.TestCase):
	def test_employee_onboarding_incomplete_task(self):
		if finergy.db.exists("Employee Onboarding", {"employee_name": "Test Researcher"}):
			finergy.delete_doc("Employee Onboarding", {"employee_name": "Test Researcher"})
		finergy.db.sql("delete from `tabEmployee Onboarding`")
		project = "Employee Onboarding : test@researcher.com"
		finergy.db.sql("delete from tabProject where name=%s", project)
		finergy.db.sql("delete from tabTask where project=%s", project)
		applicant = get_job_applicant()

		job_offer = create_job_offer(job_applicant=applicant.name)
		job_offer.submit()

		onboarding = finergy.new_doc("Employee Onboarding")
		onboarding.job_applicant = applicant.name
		onboarding.job_offer = job_offer.name
		onboarding.company = "_Test Company"
		onboarding.designation = "Researcher"
		onboarding.append(
			"activities",
			{"activity_name": "Assign ID Card", "role": "HR User", "required_for_employee_creation": 1},
		)
		onboarding.append("activities", {"activity_name": "Assign a laptop", "role": "HR User"})
		onboarding.status = "Pending"
		onboarding.insert()
		onboarding.submit()

		project_name = finergy.db.get_value("Project", onboarding.project, "project_name")
		self.assertEqual(project_name, "Employee Onboarding : test@researcher.com")

		# don't allow making employee if onboarding is not complete
		self.assertRaises(IncompleteTaskError, make_employee, onboarding.name)

		# complete the task
		project = finergy.get_doc("Project", onboarding.project)
		for task in finergy.get_all("Task", dict(project=project.name)):
			task = finergy.get_doc("Task", task.name)
			task.status = "Completed"
			task.save()

		# make employee
		onboarding.reload()
		employee = make_employee(onboarding.name)
		employee.first_name = employee.employee_name
		employee.date_of_joining = nowdate()
		employee.date_of_birth = "1990-05-08"
		employee.gender = "Female"
		employee.insert()
		self.assertEqual(employee.employee_name, "Test Researcher")


def get_job_applicant():
	if finergy.db.exists("Job Applicant", "test@researcher.com"):
		return finergy.get_doc("Job Applicant", "test@researcher.com")
	applicant = finergy.new_doc("Job Applicant")
	applicant.applicant_name = "Test Researcher"
	applicant.email_id = "test@researcher.com"
	applicant.designation = "Researcher"
	applicant.status = "Open"
	applicant.cover_letter = "I am a great Researcher."
	applicant.insert()
	return applicant


def _set_up():
	for doctype in ["Employee Onboarding"]:
		finergy.db.sql("delete from `tab{doctype}`".format(doctype=doctype))

	project = "Employee Onboarding : Test Researcher - test@researcher.com"
	finergy.db.sql("delete from tabProject where name=%s", project)
	finergy.db.sql("delete from tabTask where project=%s", project)
