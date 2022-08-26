// Copyright (c) 2020, Finergy Reporting Solutions SAS and Contributors
// License: GNU General Public License v3. See license.txt
finergy.views.calendar["Opportunity"] = {
	field_map: {
		"start": "contact_date",
		"end": "contact_date",
		"id": "name",
		"title": "customer_name",
		"allDay": "allDay"
    },
	options: {
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month'
		}
    },
    get_events_method: 'capkpi.crm.doctype.opportunity.opportunity.get_events'
}
