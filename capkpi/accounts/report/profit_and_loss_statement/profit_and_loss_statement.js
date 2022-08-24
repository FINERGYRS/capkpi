// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt


finergy.require("assets/capkpi/js/financial_statements.js", function() {
	finergy.query_reports["Profit and Loss Statement"] = $.extend({},
		capkpi.financial_statements);

	capkpi.utils.add_dimensions('Profit and Loss Statement', 10);

	finergy.query_reports["Profit and Loss Statement"]["filters"].push(
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return finergy.db.get_link_options('Project', txt);
			}
		},
		{
			"fieldname": "include_default_book_entries",
			"label": __("Include Default Book Entries"),
			"fieldtype": "Check",
			"default": 1
		}
	);
});
