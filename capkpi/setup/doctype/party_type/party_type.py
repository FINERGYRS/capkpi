# Copyright (c) 2015, Finergy Technologies and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class PartyType(Document):
	pass


@finergy.whitelist()
@finergy.validate_and_sanitize_search_inputs
def get_party_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ""
	if filters and filters.get("account"):
		account_type = finergy.db.get_value("Account", filters.get("account"), "account_type")
		cond = "and account_type = '%s'" % account_type

	return finergy.db.sql(
		"""select name from `tabParty Type`
			where `{key}` LIKE %(txt)s {cond}
			order by name limit %(page_len)s offset %(start)s""".format(
			key=searchfield, cond=cond
		),
		{"txt": "%" + txt + "%", "start": start, "page_len": page_len},
	)
