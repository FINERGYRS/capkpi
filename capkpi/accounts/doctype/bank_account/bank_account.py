# Copyright (c) 2015, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy
from finergy import _
from finergy.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
from finergy.model.document import Document


class BankAccount(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)

	def autoname(self):
		self.name = self.account_name + " - " + self.bank

	def on_trash(self):
		delete_contact_and_address("BankAccount", self.name)

	def validate(self):
		self.validate_company()
		self.validate_iban()

	def validate_company(self):
		if self.is_company_account and not self.company:
			finergy.throw(_("Company is manadatory for company account"))

	def validate_iban(self):
		"""
		Algorithm: https://en.wikipedia.org/wiki/International_Bank_Account_Number#Validating_the_IBAN
		"""
		# IBAN field is optional
		if not self.iban:
			return

		def encode_char(c):
			# Position in the alphabet (A=1, B=2, ...) plus nine
			return str(9 + ord(c) - 64)

		# remove whitespaces, upper case to get the right number from ord()
		iban = "".join(self.iban.split(" ")).upper()

		# Move country code and checksum from the start to the end
		flipped = iban[4:] + iban[:4]

		# Encode characters as numbers
		encoded = [encode_char(c) if ord(c) >= 65 and ord(c) <= 90 else c for c in flipped]

		try:
			to_check = int("".join(encoded))
		except ValueError:
			finergy.throw(_("IBAN is not valid"))

		if to_check % 97 != 1:
			finergy.throw(_("IBAN is not valid"))


@finergy.whitelist()
def make_bank_account(doctype, docname):
	doc = finergy.new_doc("Bank Account")
	doc.party_type = doctype
	doc.party = docname
	doc.is_default = 1

	return doc


@finergy.whitelist()
def get_party_bank_account(party_type, party):
	return finergy.db.get_value(party_type, party, "default_bank_account")


@finergy.whitelist()
def get_bank_account_details(bank_account):
	return finergy.db.get_value(
		"Bank Account", bank_account, ["account", "bank", "bank_account_no"], as_dict=1
	)
