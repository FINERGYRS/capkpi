import os

import finergy
from finergy import _


def execute():
	finergy.reload_doc("email", "doctype", "email_template")
	finergy.reload_doc("stock", "doctype", "delivery_settings")

	if not finergy.db.exists("Email Template", _("Dispatch Notification")):
		base_path = finergy.get_app_path("capkpi", "stock", "doctype")
		response = finergy.read_file(
			os.path.join(base_path, "delivery_trip/dispatch_notification_template.html")
		)

		finergy.get_doc(
			{
				"doctype": "Email Template",
				"name": _("Dispatch Notification"),
				"response": response,
				"subject": _("Your order is out for delivery!"),
				"owner": finergy.session.user,
			}
		).insert(ignore_permissions=True)

	delivery_settings = finergy.get_doc("Delivery Settings")
	delivery_settings.dispatch_template = _("Dispatch Notification")
	delivery_settings.flags.ignore_links = True
	delivery_settings.save()
