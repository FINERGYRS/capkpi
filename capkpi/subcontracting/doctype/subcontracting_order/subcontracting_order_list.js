// Copyright (c) 2022, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.listview_settings['Subcontracting Order'] = {
	get_indicator: function (doc) {
		const status_colors = {
			"Draft": "grey",
			"Open": "orange",
			"Partially Received": "yellow",
			"Completed": "green",
			"Partial Material Transferred": "purple",
			"Material Transferred": "blue",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};