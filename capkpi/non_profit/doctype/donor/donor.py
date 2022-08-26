# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.contacts.address_and_contact import load_address_and_contact
from finergy.model.document import Document


class Donor(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def validate(self):
		from finergy.utils import validate_email_address

		if self.email:
			validate_email_address(self.email.strip(), True)
