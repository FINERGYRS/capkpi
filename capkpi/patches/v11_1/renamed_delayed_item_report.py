# Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	for report in ["Delayed Order Item Summary", "Delayed Order Summary"]:
		if finergy.db.exists("Report", report):
			finergy.delete_doc("Report", report)
