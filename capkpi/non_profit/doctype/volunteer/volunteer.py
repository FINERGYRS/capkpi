# Copyright (c) 2017, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from finergy.contacts.address_and_contact import load_address_and_contact
from finergy.model.document import Document


class Volunteer(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
