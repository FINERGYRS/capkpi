// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Project Summary"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": finergy.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname": "is_active",
			"label": __("Is Active"),
			"fieldtype": "Select",
			"options": "\nYes\nNo",
			"default": "Yes",
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nOpen\nCompleted\nCancelled",
			"default": "Open"
		},
		{
			"fieldname": "project_type",
			"label": __("Project Type"),
			"fieldtype": "Link",
			"options": "Project Type"
		},
		{
			"fieldname": "priority",
			"label": __("Priority"),
			"fieldtype": "Select",
			"options": "\nLow\nMedium\nHigh"
		}
	]
};
