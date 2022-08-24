# Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from finergy.model.document import Document


class Bank(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def on_trash(self):
		delete_contact_and_address("Bank", self.name)
