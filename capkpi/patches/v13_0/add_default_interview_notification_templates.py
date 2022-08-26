import os

import finergy
from finergy import _


def execute():
	if not finergy.db.exists("Email Template", _("Interview Reminder")):
		base_path = finergy.get_app_path("capkpi", "hr", "doctype")
		response = finergy.read_file(
			os.path.join(base_path, "interview/interview_reminder_notification_template.html")
		)

		finergy.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Interview Reminder"),
				"response": response,
				"subject": _("Interview Reminder"),
				"owner": finergy.session.user,
			}
		).insert(ignore_permissions=True)

	if not finergy.db.exists("Email Template", _("Interview Feedback Reminder")):
		base_path = finergy.get_app_path("capkpi", "hr", "doctype")
		response = finergy.read_file(
			os.path.join(base_path, "interview/interview_feedback_reminder_template.html")
		)

		finergy.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Interview Feedback Reminder"),
				"response": response,
				"subject": _("Interview Feedback Reminder"),
				"owner": finergy.session.user,
			}
		).insert(ignore_permissions=True)

	hr_settings = finergy.get_doc("HR Settings")
	hr_settings.interview_reminder_template = _("Interview Reminder")
	hr_settings.feedback_reminder_notification_template = _("Interview Feedback Reminder")
	hr_settings.flags.ignore_links = True
	hr_settings.save()
