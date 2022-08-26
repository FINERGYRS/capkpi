# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doctype("Quotation")
	finergy.db.sql(""" UPDATE `tabQuotation` set party_name = lead WHERE quotation_to = 'Lead' """)
	finergy.db.sql(
		""" UPDATE `tabQuotation` set party_name = customer WHERE quotation_to = 'Customer' """
	)

	finergy.reload_doctype("Opportunity")
	finergy.db.sql(
		""" UPDATE `tabOpportunity` set party_name = lead WHERE opportunity_from = 'Lead' """
	)
	finergy.db.sql(
		""" UPDATE `tabOpportunity` set party_name = customer WHERE opportunity_from = 'Customer' """
	)
