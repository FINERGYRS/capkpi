# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt

# For license information, please see license.txt


import finergy
from finergy.model.document import Document
from finergy.model.rename_doc import bulk_rename


class RenameTool(Document):
	pass


@finergy.whitelist()
def get_doctypes():
	return finergy.db.sql_list(
		"""select name from tabDocType
		where allow_rename=1 and module!='Core' order by name"""
	)


@finergy.whitelist()
def upload(select_doctype=None, rows=None):
	from finergy.utils.csvutils import read_csv_content_from_attached_file

	if not select_doctype:
		select_doctype = finergy.form_dict.select_doctype

	if not finergy.has_permission(select_doctype, "write"):
		raise finergy.PermissionError

	rows = read_csv_content_from_attached_file(finergy.get_doc("Rename Tool", "Rename Tool"))

	return bulk_rename(select_doctype, rows=rows)
