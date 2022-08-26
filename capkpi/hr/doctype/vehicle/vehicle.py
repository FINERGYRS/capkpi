# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils import getdate


class Vehicle(Document):
	def validate(self):
		if getdate(self.start_date) > getdate(self.end_date):
			finergy.throw(_("Insurance Start date should be less than Insurance End date"))
		if getdate(self.carbon_check_date) > getdate():
			finergy.throw(_("Last carbon check date cannot be a future date"))


def get_timeline_data(doctype, name):
	"""Return timeline for vehicle log"""
	return dict(
		finergy.db.sql(
			"""select unix_timestamp(date), count(*)
	from `tabVehicle Log` where license_plate=%s
	and date > date_sub(curdate(), interval 1 year)
	group by date""",
			name,
		)
	)
