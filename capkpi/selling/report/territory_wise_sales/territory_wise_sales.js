// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */


finergy.query_reports["Territory-wise Sales"] = {
	"breadcrumb":"Selling",
	"filters": [
		{
			fieldname:"transaction_date",
			label: __("Transaction Date"),
			fieldtype: "DateRange",
			default: [finergy.datetime.add_months(finergy.datetime.get_today(),-1), finergy.datetime.get_today()],
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
		}
	]
};
