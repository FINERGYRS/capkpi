// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.require("assets/capkpi/js/sales_trends_filters.js", function() {
	finergy.query_reports["Sales Order Trends"] = {
		filters: capkpi.get_sales_trends_filters()
	}
});
