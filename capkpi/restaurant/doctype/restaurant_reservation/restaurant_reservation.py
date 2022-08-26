# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from datetime import timedelta

from finergy.model.document import Document
from finergy.utils import get_datetime


class RestaurantReservation(Document):
	def validate(self):
		if not self.reservation_end_time:
			self.reservation_end_time = get_datetime(self.reservation_time) + timedelta(hours=1)
