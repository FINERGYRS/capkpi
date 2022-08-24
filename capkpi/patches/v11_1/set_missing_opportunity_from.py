import finergy


def execute():

	finergy.reload_doctype("Opportunity")
	if finergy.db.has_column("Opportunity", "enquiry_from"):
		finergy.db.sql(
			""" UPDATE `tabOpportunity` set opportunity_from = enquiry_from
			where ifnull(opportunity_from, '') = '' and ifnull(enquiry_from, '') != ''"""
		)

	if finergy.db.has_column("Opportunity", "lead") and finergy.db.has_column(
		"Opportunity", "enquiry_from"
	):
		finergy.db.sql(
			""" UPDATE `tabOpportunity` set party_name = lead
			where enquiry_from = 'Lead' and ifnull(party_name, '') = '' and ifnull(lead, '') != ''"""
		)

	if finergy.db.has_column("Opportunity", "customer") and finergy.db.has_column(
		"Opportunity", "enquiry_from"
	):
		finergy.db.sql(
			""" UPDATE `tabOpportunity` set party_name = customer
			 where enquiry_from = 'Customer' and ifnull(party_name, '') = '' and ifnull(customer, '') != ''"""
		)
