// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Training Event', {
	onload_post_render: function (frm) {
		frm.get_field("employees").grid.set_multiple_add("employee");
	},
	refresh: function (frm) {
		if (!frm.doc.__islocal) {
			frm.add_custom_button(__("Training Result"), function () {
				finergy.route_options = {
					training_event: frm.doc.name
				};
				finergy.set_route("List", "Training Result");
			});
			frm.add_custom_button(__("Training Feedback"), function () {
				finergy.route_options = {
					training_event: frm.doc.name
				};
				finergy.set_route("List", "Training Feedback");
			});
		}
		frm.events.set_employee_query(frm);
	},

	set_employee_query: function(frm) {
		let emp = [];
		for (let d in frm.doc.employees) {
			if (frm.doc.employees[d].employee) {
				emp.push(frm.doc.employees[d].employee);
			}
		}
		frm.set_query("employee", "employees", function () {
			return {
				filters: {
					name: ["NOT IN", emp],
					status: "Active"
				}
			};
		});
	}
});

finergy.ui.form.on("Training Event Employee", {
	employee: function(frm) {
		frm.events.set_employee_query(frm);
	}
});
