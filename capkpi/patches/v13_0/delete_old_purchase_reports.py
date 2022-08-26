# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy

from capkpi.accounts.utils import check_and_delete_linked_reports


def execute():
	reports_to_delete = [
		"Requested Items To Be Ordered",
		"Purchase Order Items To Be Received or Billed",
		"Purchase Order Items To Be Received",
		"Purchase Order Items To Be Billed",
	]

	for report in reports_to_delete:
		if finergy.db.exists("Report", report):
			delete_auto_email_reports(report)
			check_and_delete_linked_reports(report)

			finergy.delete_doc("Report", report)


def delete_auto_email_reports(report):
	"""Check for one or multiple Auto Email Reports and delete"""
	auto_email_reports = finergy.db.get_values("Auto Email Report", {"report": report}, ["name"])
	for auto_email_report in auto_email_reports:
		finergy.delete_doc("Auto Email Report", auto_email_report[0])
