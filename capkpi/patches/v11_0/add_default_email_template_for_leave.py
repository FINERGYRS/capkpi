import os

import finergy
from finergy import _


def execute():
	finergy.reload_doc("email", "doctype", "email_template")

	if not finergy.db.exists("Email Template", _("Leave Approval Notification")):
		base_path = finergy.get_app_path("capkpi", "hr", "doctype")
		response = finergy.read_file(
			os.path.join(base_path, "leave_application/leave_application_email_template.html")
		)
		finergy.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Leave Approval Notification"),
				"response": response,
				"subject": _("Leave Approval Notification"),
				"owner": finergy.session.user,
			}
		).insert(ignore_permissions=True)

	if not finergy.db.exists("Email Template", _("Leave Status Notification")):
		base_path = finergy.get_app_path("capkpi", "hr", "doctype")
		response = finergy.read_file(
			os.path.join(base_path, "leave_application/leave_application_email_template.html")
		)
		finergy.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Leave Status Notification"),
				"response": response,
				"subject": _("Leave Status Notification"),
				"owner": finergy.session.user,
			}
		).insert(ignore_permissions=True)
