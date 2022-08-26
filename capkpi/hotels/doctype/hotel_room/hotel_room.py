# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class HotelRoom(Document):
	def validate(self):
		if not self.capacity:
			self.capacity, self.extra_bed_capacity = finergy.db.get_value(
				"Hotel Room Type", self.hotel_room_type, ["capacity", "extra_bed_capacity"]
			)
