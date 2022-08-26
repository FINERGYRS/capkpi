// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

// render
finergy.listview_settings['POS Opening Entry'] = {
	get_indicator: function(doc) {
		var status_color = {
			"Draft": "red",
			"Open": "orange",
			"Closed": "green",
			"Cancelled": "red"

		};
		return [__(doc.status), status_color[doc.status], "status,=,"+doc.status];
	}
};
