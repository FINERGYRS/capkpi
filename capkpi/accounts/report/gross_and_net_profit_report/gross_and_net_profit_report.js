// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
/* eslint-disable */

finergy.query_reports["Gross and Net Profit Report"] = {
	"filters": [

	]
}
finergy.require("assets/capkpi/js/financial_statements.js", function() {
	finergy.query_reports["Gross and Net Profit Report"] = $.extend({},
		capkpi.financial_statements);

	finergy.query_reports["Gross and Net Profit Report"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return finergy.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "accumulated_values",
			"label": __("Accumulated Values"),
			"fieldtype": "Check"
		}
	);
});
