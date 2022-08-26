# Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
# MIT License. See license.txt


import finergy


def execute():
	finergy.reload_doc("hr", "doctype", "employee")

	if finergy.db.has_column("Employee", "reason_for_resignation"):
		finergy.db.sql(
			""" UPDATE `tabEmployee`
            SET reason_for_leaving = reason_for_resignation
            WHERE status = 'Left' and reason_for_leaving is null and reason_for_resignation is not null
        """
		)
