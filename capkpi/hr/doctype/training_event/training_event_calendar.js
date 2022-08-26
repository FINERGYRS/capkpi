// Copyright (c) 2015, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt

finergy.views.calendar["Training Event"] = {
	field_map: {
		"start": "start_time",
		"end": "end_time",
		"id": "name",
		"title": "event_name",
		"allDay": "allDay"
	},
	gantt: true,
	get_events_method: "finergy.desk.calendar.get_events",
}
