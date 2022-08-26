# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.model.document import Document


class TrainingFeedback(Document):
	def validate(self):
		training_event = finergy.get_doc("Training Event", self.training_event)
		if training_event.docstatus != 1:
			finergy.throw(_("{0} must be submitted").format(_("Training Event")))

		emp_event_details = finergy.db.get_value(
			"Training Event Employee",
			{"parent": self.training_event, "employee": self.employee},
			["name", "attendance"],
			as_dict=True,
		)

		if not emp_event_details:
			finergy.throw(
				_("Employee {0} not found in Training Event Participants.").format(
					finergy.bold(self.employee_name)
				)
			)

		if emp_event_details.attendance == "Absent":
			finergy.throw(_("Feedback cannot be recorded for an absent Employee."))

	def on_submit(self):
		employee = finergy.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			finergy.db.set_value("Training Event Employee", employee, "status", "Feedback Submitted")

	def on_cancel(self):
		employee = finergy.db.get_value(
			"Training Event Employee", {"parent": self.training_event, "employee": self.employee}
		)

		if employee:
			finergy.db.set_value("Training Event Employee", employee, "status", "Completed")
