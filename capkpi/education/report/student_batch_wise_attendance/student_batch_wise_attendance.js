// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.query_reports["Student Batch-Wise Attendance"] = {
	"filters": [{
		"fieldname": "date",
		"label": __("Date"),
		"fieldtype": "Date",
		"default": finergy.datetime.get_today(),
		"reqd": 1
	}]
}
