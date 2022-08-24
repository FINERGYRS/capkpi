# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# MIT License. See license.txt


import finergy
from finergy.model.utils.rename_field import rename_field


def execute():
	"""add value to email_id column from email"""

	if finergy.db.has_column("Member", "email"):
		# Get all members
		for member in finergy.db.get_all("Member", pluck="name"):
			# Check if email_id already exists
			if not finergy.db.get_value("Member", member, "email_id"):
				# fetch email id from the user linked field email
				email = finergy.db.get_value("Member", member, "email")

				# Set the value for it
				finergy.db.set_value("Member", member, "email_id", email)

	if finergy.db.exists("DocType", "Membership Settings"):
		rename_field("Membership Settings", "enable_auto_invoicing", "enable_invoicing")
