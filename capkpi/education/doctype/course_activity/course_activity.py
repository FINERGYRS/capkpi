# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class CourseActivity(Document):
	def validate(self):
		self.check_if_enrolled()

	def check_if_enrolled(self):
		if finergy.db.exists("Course Enrollment", self.enrollment):
			return True
		else:
			finergy.throw(_("Course Enrollment {0} does not exists").format(self.enrollment))
