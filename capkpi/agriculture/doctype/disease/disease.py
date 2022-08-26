# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class Disease(Document):
	def validate(self):
		max_period = 0
		for task in self.treatment_task:
			# validate start_day is not > end_day
			if task.start_day > task.end_day:
				finergy.throw(_("Start day is greater than end day in task '{0}'").format(task.task_name))
			# to calculate the period of the Crop Cycle
			if task.end_day > max_period:
				max_period = task.end_day
		self.treatment_period = max_period
