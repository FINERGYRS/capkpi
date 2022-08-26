import finergy


def execute():
	company = finergy.db.get_single_value("Global Defaults", "default_company")
	doctypes = [
		"Clinical Procedure",
		"Inpatient Record",
		"Lab Test",
		"Sample Collection",
		"Patient Appointment",
		"Patient Encounter",
		"Vital Signs",
		"Therapy Session",
		"Therapy Plan",
		"Patient Assessment",
	]
	for entry in doctypes:
		if finergy.db.exists("DocType", entry):
			finergy.reload_doc("Healthcare", "doctype", entry)
			finergy.db.sql(
				"update `tab{dt}` set company = {company} where ifnull(company, '') = ''".format(
					dt=entry, company=finergy.db.escape(company)
				)
			)
