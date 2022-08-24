import finergy


def execute():
	finergy.reload_doc("crm", "doctype", "lead")
	finergy.db.sql(
		"""
		UPDATE
			`tabLead`
		SET
			title = IF(organization_lead = 1, company_name, lead_name)
	"""
	)
