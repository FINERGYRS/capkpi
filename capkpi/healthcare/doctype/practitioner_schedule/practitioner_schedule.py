# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.model.document import Document


class PractitionerSchedule(Document):
	def autoname(self):
		self.name = self.schedule_name
