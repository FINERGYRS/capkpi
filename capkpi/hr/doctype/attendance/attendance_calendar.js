// Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt
finergy.views.calendar["Attendance"] = {
	options: {
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month'
		}
	},
	get_events_method: "capkpi.hr.doctype.attendance.attendance.get_events"
};
