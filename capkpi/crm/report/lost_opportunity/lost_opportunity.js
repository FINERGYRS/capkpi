// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Lost Opportunity"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": finergy.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": finergy.datetime.add_months(finergy.datetime.get_today(), -12),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": finergy.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"lost_reason",
			"label": __("Lost Reason"),
			"fieldtype": "Link",
			"options": "Opportunity Lost Reason"
		},
		{
			"fieldname":"territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory"
		},
		{
			"fieldname":"opportunity_from",
			"label": __("Opportunity From"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query": function() {
				return {
					"filters": {
						"name": ["in", ["Customer", "Lead"]],
					}
				}
			}
		},
		{
			"fieldname":"party_name",
			"label": __("Party"),
			"fieldtype": "Dynamic Link",
			"options": "opportunity_from"
		},
	]
};
