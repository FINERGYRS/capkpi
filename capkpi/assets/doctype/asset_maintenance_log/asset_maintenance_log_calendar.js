// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.views.calendar["Asset Maintenance Log"] = {
	field_map: {
		"start": "due_date",
		"end": "due_date",
		"id": "name",
		"title": "task",
		"allDay": "allDay",
		"progress": "progress"
	},
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "asset_name",
			"options": "Asset Maintenance",
			"label": __("Asset Maintenance")
		}
	],
	get_events_method: "finergy.desk.calendar.get_events"
};
