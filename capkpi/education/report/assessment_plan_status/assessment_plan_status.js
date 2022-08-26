// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Assessment Plan Status"] = {
	"filters": [
		{
			"fieldname":"assessment_group",
			"label": __("Assessment Group"),
			"fieldtype": "Link",
			"options": "Assessment Group",
			"get_query": function() {
				return{
					filters: {
						'is_group': 0
					}
				};
			}
		},
		{
			"fieldname":"schedule_date",
			"label": __("Scheduled Upto"),
			"fieldtype": "Date",
			"options": ""
		}

	]
}
