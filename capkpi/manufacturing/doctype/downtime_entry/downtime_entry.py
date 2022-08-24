# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.model.document import Document
from finergy.utils import time_diff_in_hours


class DowntimeEntry(Document):
	def validate(self):
		if self.from_time and self.to_time:
			self.downtime = time_diff_in_hours(self.to_time, self.from_time) * 60
