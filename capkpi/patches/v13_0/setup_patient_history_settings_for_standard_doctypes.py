import finergy

from capkpi.healthcare.setup import setup_patient_history_settings


def execute():
	if "Healthcare" not in finergy.get_active_domains():
		return

	finergy.reload_doc("healthcare", "doctype", "Inpatient Medication Order")
	finergy.reload_doc("healthcare", "doctype", "Therapy Session")
	finergy.reload_doc("healthcare", "doctype", "Clinical Procedure")
	finergy.reload_doc("healthcare", "doctype", "Patient History Settings")
	finergy.reload_doc("healthcare", "doctype", "Patient History Standard Document Type")
	finergy.reload_doc("healthcare", "doctype", "Patient History Custom Document Type")

	setup_patient_history_settings()
