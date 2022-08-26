// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.views.calendar["Leave Application"] = {
	field_map: {
		"start": "from_date",
		"end": "to_date",
		"id": "name",
		"title": "title",
		"docstatus": 1,
		"color": "color",
		"allDay": "all_day"
	},
	options: {
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month'
		}
	},
	get_events_method: "capkpi.hr.doctype.leave_application.leave_application.get_events"
}