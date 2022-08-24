# Copyright (c) 2013, Finergy Reporting Solutions SAS and contributors
# For license information, please see license.txt


from capkpi.selling.report.sales_analytics.sales_analytics import Analytics


def execute(filters=None):
	return Analytics(filters).run()
