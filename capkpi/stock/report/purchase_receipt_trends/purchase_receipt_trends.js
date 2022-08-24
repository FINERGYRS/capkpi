// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.require("assets/capkpi/js/purchase_trends_filters.js", function() {
	finergy.query_reports["Purchase Receipt Trends"] = {
		filters: capkpi.get_purchase_trends_filters()
	}
});
