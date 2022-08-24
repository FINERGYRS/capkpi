# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	if finergy.db.exists("DocType", "Scheduling Tool"):
		finergy.delete_doc("DocType", "Scheduling Tool", ignore_permissions=True)
