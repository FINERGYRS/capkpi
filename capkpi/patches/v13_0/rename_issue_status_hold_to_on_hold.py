# Copyright (c) 2020, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	if finergy.db.exists("DocType", "Issue"):
		finergy.reload_doc("support", "doctype", "issue")
		rename_status()


def rename_status():
	finergy.db.sql(
		"""
		UPDATE
			`tabIssue`
		SET
			status = 'On Hold'
		WHERE
			status = 'Hold'
	"""
	)
