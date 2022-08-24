# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class SupplierScorecardStanding(Document):
	pass


@finergy.whitelist()
def get_scoring_standing(standing_name):
	standing = finergy.get_doc("Supplier Scorecard Standing", standing_name)

	return standing


@finergy.whitelist()
def get_standings_list():
	standings = finergy.db.sql(
		"""
		SELECT
			scs.name
		FROM
			`tabSupplier Scorecard Standing` scs""",
		{},
		as_dict=1,
	)

	return standings
