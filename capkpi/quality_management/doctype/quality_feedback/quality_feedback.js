// Copyright (c) 2019, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Quality Feedback', {
	template: function(frm) {
		if (frm.doc.template) {
			frm.call('set_parameters');
		}
	}
});
