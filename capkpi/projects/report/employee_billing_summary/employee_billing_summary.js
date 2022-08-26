// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Employee Billing Summary"] = {
	"filters": [
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options: "Employee",
			reqd: 1
		},
		{
			fieldname:"from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: finergy.datetime.add_months(finergy.datetime.month_start(), -1),
			reqd: 1
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: finergy.datetime.add_days(finergy.datetime.month_start(), -1),
			reqd: 1
		},
	]
}
