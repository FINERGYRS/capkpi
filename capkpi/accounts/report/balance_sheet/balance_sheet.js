// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.require("assets/capkpi/js/financial_statements.js", function() {
	finergy.query_reports["Balance Sheet"] = $.extend({}, capkpi.financial_statements);

	capkpi.utils.add_dimensions('Balance Sheet', 10);

	finergy.query_reports["Balance Sheet"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check",
		"default": 1
	});

	finergy.query_reports["Balance Sheet"]["filters"].push({
		"fieldname": "include_default_book_entries",
		"label": __("Include Default Book Entries"),
		"fieldtype": "Check",
		"default": 1
	});
});
