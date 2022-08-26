# Copyright (c) 2013, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


import finergy

from capkpi.projects.report.billing_summary import get_columns, get_data


def execute(filters=None):
	filters = finergy._dict(filters or {})
	columns = get_columns()

	data = get_data(filters)
	return columns, data
