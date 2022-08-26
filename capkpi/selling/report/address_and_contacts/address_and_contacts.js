// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Address And Contacts"] = {
	"filters": [
		{
			"reqd": 1,
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"get_query": function() {
				return {
					"filters": {
						"name": ["in","Customer,Supplier,Sales Partner"],
					}
				}
			}
		},
		{
			"fieldname":"party_name",
			"label": __("Party Name"),
			"fieldtype": "Dynamic Link",
			"get_options": function() {
				let party_type = finergy.query_report.get_filter_value('party_type');
				if(!party_type) {
					finergy.throw(__("Please select Party Type first"));
				}
				return party_type;
			}
		}
	]
}
