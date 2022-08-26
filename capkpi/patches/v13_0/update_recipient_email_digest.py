# Copyright (c) 2020, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	finergy.reload_doc("setup", "doctype", "Email Digest")
	finergy.reload_doc("setup", "doctype", "Email Digest Recipient")
	email_digests = finergy.db.get_list("Email Digest", fields=["name", "recipient_list"])
	for email_digest in email_digests:
		if email_digest.recipient_list:
			for recipient in email_digest.recipient_list.split("\n"):
				if finergy.db.exists("User", recipient):
					doc = finergy.get_doc(
						{
							"doctype": "Email Digest Recipient",
							"parenttype": "Email Digest",
							"parentfield": "recipients",
							"parent": email_digest.name,
							"recipient": recipient,
						}
					)
					doc.insert()
