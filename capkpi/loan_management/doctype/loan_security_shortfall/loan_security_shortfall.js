// Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Loan Security Shortfall', {
	refresh: function(frm) {
		frm.add_custom_button(__("Add Loan Security"), function() {
			frm.trigger('shortfall_action');
		});
	},

	shortfall_action: function(frm) {
		finergy.call({
			method: "capkpi.loan_management.doctype.loan_security_shortfall.loan_security_shortfall.add_security",
			args: {
				'loan': frm.doc.loan
			},
			callback: function(r) {
				if (r.message) {
					let doc = finergy.model.sync(r.message)[0];
					finergy.set_route("Form", doc.doctype, doc.name);
				}
			}
		});
	}
});
