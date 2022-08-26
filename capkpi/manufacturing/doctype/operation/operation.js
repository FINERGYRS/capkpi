// Copyright (c) 2016, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Operation', {
	setup: function(frm) {
		frm.set_query('operation', 'sub_operations', function() {
			return {
				filters: {
					'name': ['not in', [frm.doc.name]]
				}
			};
		});
	}
});
