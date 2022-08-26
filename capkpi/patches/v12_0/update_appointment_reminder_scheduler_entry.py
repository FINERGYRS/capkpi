import finergy


def execute():
	job = finergy.db.exists("Scheduled Job Type", "patient_appointment.send_appointment_reminder")
	if job:
		method = (
			"capkpi.healthcare.doctype.patient_appointment.patient_appointment.send_appointment_reminder"
		)
		finergy.db.set_value("Scheduled Job Type", job, "method", method)
