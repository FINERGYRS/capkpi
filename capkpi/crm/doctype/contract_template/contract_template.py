# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import json

import finergy
from finergy.model.document import Document
from finergy.utils.jinja import validate_template
from six import string_types


class ContractTemplate(Document):
	def validate(self):
		if self.contract_terms:
			validate_template(self.contract_terms)


@finergy.whitelist()
def get_contract_template(template_name, doc):
	if isinstance(doc, string_types):
		doc = json.loads(doc)

	contract_template = finergy.get_doc("Contract Template", template_name)
	contract_terms = None

	if contract_template.contract_terms:
		contract_terms = finergy.render_template(contract_template.contract_terms, doc)

	return {"contract_template": contract_template, "contract_terms": contract_terms}
