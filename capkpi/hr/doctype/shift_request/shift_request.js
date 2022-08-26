// Copyright (c) 2018, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Shift Request', {
	setup: function(frm) {
		frm.set_query("approver", function() {
			return {
				query: "capkpi.hr.doctype.department_approver.department_approver.get_approvers",
				filters: {
					employee: frm.doc.employee,
					doctype: frm.doc.doctype
				}
			};
		});
		frm.set_query("employee", capkpi.queries.employee);
	},
});
