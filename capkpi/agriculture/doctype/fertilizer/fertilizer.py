# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy.model.document import Document


class Fertilizer(Document):
	@finergy.whitelist()
	def load_contents(self):
		docs = finergy.get_all("Agriculture Analysis Criteria", filters={"linked_doctype": "Fertilizer"})
		for doc in docs:
			self.append("fertilizer_contents", {"title": str(doc.name)})
