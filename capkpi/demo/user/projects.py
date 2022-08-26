# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy
from finergy.utils import flt
from finergy.utils.make_random import get_random

import capkpi
from capkpi.demo.user.hr import make_sales_invoice_for_timesheet
from capkpi.projects.doctype.timesheet.test_timesheet import make_timesheet


def run_projects(current_date):
	finergy.set_user(finergy.db.get_global("demo_projects_user"))
	if finergy.db.get_global("demo_projects_user"):
		make_project(current_date)
		make_timesheet_for_projects(current_date)
		close_tasks(current_date)


def make_timesheet_for_projects(current_date):
	for data in finergy.get_all(
		"Task", ["name", "project"], {"status": "Open", "exp_end_date": ("<", current_date)}
	):
		employee = get_random("Employee")
		ts = make_timesheet(
			employee,
			simulate=True,
			billable=1,
			company=capkpi.get_default_company(),
			activity_type=get_random("Activity Type"),
			project=data.project,
			task=data.name,
		)

		if flt(ts.total_billable_amount) > 0.0:
			make_sales_invoice_for_timesheet(ts.name)
			finergy.db.commit()


def close_tasks(current_date):
	for task in finergy.get_all(
		"Task", ["name"], {"status": "Open", "exp_end_date": ("<", current_date)}
	):
		task = finergy.get_doc("Task", task.name)
		task.status = "Completed"
		task.save()


def make_project(current_date):
	if not finergy.db.exists(
		"Project", "New Product Development " + current_date.strftime("%Y-%m-%d")
	):
		project = finergy.get_doc(
			{
				"doctype": "Project",
				"project_name": "New Product Development " + current_date.strftime("%Y-%m-%d"),
			}
		)
		project.insert()
