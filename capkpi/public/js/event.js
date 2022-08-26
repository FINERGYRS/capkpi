// Copyright (c) 2018, Finergy Reporting Solutions SAS and Contributors
// MIT License. See license.txt
finergy.provide("finergy.desk");

finergy.ui.form.on("Event", {
	refresh: function(frm) {
		frm.set_query('reference_doctype', "event_participants", function() {
			return {
				"filters": {
					"name": ["in", ["Contact", "Lead", "Customer", "Supplier", "Employee", "Sales Partner"]]
				}
			};
		});

		frm.add_custom_button(__('Add Leads'), function() {
			new finergy.desk.eventParticipants(frm, "Lead");
		}, __("Add Participants"));

		frm.add_custom_button(__('Add Customers'), function() {
			new finergy.desk.eventParticipants(frm, "Customer");
		}, __("Add Participants"));

		frm.add_custom_button(__('Add Suppliers'), function() {
			new finergy.desk.eventParticipants(frm, "Supplier");
		}, __("Add Participants"));

		frm.add_custom_button(__('Add Employees'), function() {
			new finergy.desk.eventParticipants(frm, "Employee");
		}, __("Add Participants"));

		frm.add_custom_button(__('Add Sales Partners'), function() {
			new finergy.desk.eventParticipants(frm, "Sales Partners");
		}, __("Add Participants"));
	}
});
