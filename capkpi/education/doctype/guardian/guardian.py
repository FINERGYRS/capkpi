# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document
from finergy.utils.csvutils import getlink


class Guardian(Document):
	def __setup__(self):
		self.onload()

	def onload(self):
		"""Load Students for quick view"""
		self.load_students()

	def load_students(self):
		"""Load `students` from the database"""
		self.students = []
		students = finergy.get_all("Student Guardian", filters={"guardian": self.name}, fields=["parent"])
		for student in students:
			self.append(
				"students",
				{
					"student": student.parent,
					"student_name": finergy.db.get_value("Student", student.parent, "title"),
				},
			)

	def validate(self):
		self.students = []


@finergy.whitelist()
def invite_guardian(guardian):
	guardian_doc = finergy.get_doc("Guardian", guardian)
	if not guardian_doc.email_address:
		finergy.throw(_("Please set Email Address"))
	else:
		guardian_as_user = finergy.get_value("User", dict(email=guardian_doc.email_address))
		if guardian_as_user:
			finergy.msgprint(_("User {0} already exists").format(getlink("User", guardian_as_user)))
			return guardian_as_user
		else:
			user = finergy.get_doc(
				{
					"doctype": "User",
					"first_name": guardian_doc.guardian_name,
					"email": guardian_doc.email_address,
					"user_type": "Website User",
					"send_welcome_email": 1,
				}
			).insert(ignore_permissions=True)
			finergy.msgprint(_("User {0} created").format(getlink("User", user.name)))
			return user.name
