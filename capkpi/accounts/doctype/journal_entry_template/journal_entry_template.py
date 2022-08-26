# Copyright (c) 2020, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class JournalEntryTemplate(Document):
	pass


@finergy.whitelist()
def get_naming_series():
	return finergy.get_meta("Journal Entry").get_field("naming_series").options
