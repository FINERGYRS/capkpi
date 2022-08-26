# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import json
import os
import random

import finergy
import finergy.utils
from finergy import _
from finergy.utils.make_random import add_random_children


def make_sample_data(domains, make_dependent=False):
	"""Create a few opportunities, quotes, material requests, issues, todos, projects
	to help the user get started"""

	if make_dependent:
		items = finergy.get_all("Item", {"is_sales_item": 1})
		customers = finergy.get_all("Customer")
		warehouses = finergy.get_all("Warehouse")

		if items and customers:
			for i in range(3):
				customer = random.choice(customers).name
				make_opportunity(items, customer)
				make_quote(items, customer)

		if items and warehouses:
			make_material_request(finergy.get_all("Item"))

	make_projects(domains)
	import_notification()


def make_opportunity(items, customer):
	b = finergy.get_doc(
		{
			"doctype": "Opportunity",
			"opportunity_from": "Customer",
			"customer": customer,
			"opportunity_type": _("Sales"),
			"with_items": 1,
		}
	)

	add_random_children(
		b, "items", rows=len(items), randomize={"qty": (1, 5), "item_code": ["Item"]}, unique="item_code"
	)

	b.insert(ignore_permissions=True)

	b.add_comment("Comment", text="This is a dummy record")


def make_quote(items, customer):
	qtn = finergy.get_doc(
		{
			"doctype": "Quotation",
			"quotation_to": "Customer",
			"party_name": customer,
			"order_type": "Sales",
		}
	)

	add_random_children(
		qtn,
		"items",
		rows=len(items),
		randomize={"qty": (1, 5), "item_code": ["Item"]},
		unique="item_code",
	)

	qtn.insert(ignore_permissions=True)

	qtn.add_comment("Comment", text="This is a dummy record")


def make_material_request(items):
	for i in items:
		mr = finergy.get_doc(
			{
				"doctype": "Material Request",
				"material_request_type": "Purchase",
				"schedule_date": finergy.utils.add_days(finergy.utils.nowdate(), 7),
				"items": [
					{
						"schedule_date": finergy.utils.add_days(finergy.utils.nowdate(), 7),
						"item_code": i.name,
						"qty": 10,
					}
				],
			}
		)
		mr.insert()
		mr.submit()

		mr.add_comment("Comment", text="This is a dummy record")


def make_issue():
	pass


def make_projects(domains):
	current_date = finergy.utils.nowdate()
	project = finergy.get_doc(
		{
			"doctype": "Project",
			"project_name": "CapKPI Implementation",
		}
	)

	tasks = [
		{
			"title": "Explore CapKPI",
			"start_date": current_date,
			"end_date": current_date,
			"file": "explore.md",
		}
	]

	if "Education" in domains:
		tasks += [
			{
				"title": _("Setup your Institute in CapKPI"),
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 1),
				"file": "education_masters.md",
			},
			{
				"title": "Setup Master Data",
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 1),
				"file": "education_masters.md",
			},
		]

	else:
		tasks += [
			{
				"title": "Setup Your Company",
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 1),
				"file": "masters.md",
			},
			{
				"title": "Start Tracking your Sales",
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 2),
				"file": "sales.md",
			},
			{
				"title": "Start Managing Purchases",
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 3),
				"file": "purchase.md",
			},
			{
				"title": "Import Data",
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 4),
				"file": "import_data.md",
			},
			{
				"title": "Go Live!",
				"start_date": current_date,
				"end_date": finergy.utils.add_days(current_date, 5),
				"file": "go_live.md",
			},
		]

	for t in tasks:
		with open(os.path.join(os.path.dirname(__file__), "tasks", t["file"])) as f:
			t["description"] = finergy.utils.md_to_html(f.read())
			del t["file"]

		project.append("tasks", t)

	project.insert(ignore_permissions=True)


def import_notification():
	"""Import notification for task start"""
	with open(os.path.join(os.path.dirname(__file__), "tasks/task_alert.json")) as f:
		notification = finergy.get_doc(json.loads(f.read())[0])
		notification.insert()

	# trigger the first message!
	from finergy.email.doctype.notification.notification import trigger_daily_alerts

	trigger_daily_alerts()


def test_sample():
	finergy.db.sql("delete from `tabNotification`")
	finergy.db.sql("delete from tabProject")
	finergy.db.sql("delete from tabTask")
	make_projects("Education")
	import_notification()
