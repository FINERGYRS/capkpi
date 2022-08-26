# Copyright (c) 2019, Finergy and Contributors
# License: GNU General Public License v3. See license.txt


import finergy


def execute():
	"""Move from due_advance_amount to pending_amount"""

	if finergy.db.has_column("Employee Advance", "due_advance_amount"):
		finergy.db.sql(""" UPDATE `tabEmployee Advance` SET pending_amount=due_advance_amount """)
