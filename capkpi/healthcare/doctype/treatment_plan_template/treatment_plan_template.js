// Copyright (c) 2021, Finergy Reporting Solutions SAS and contributors
// For license information, please see license.txt

finergy.ui.form.on('Treatment Plan Template', {
	refresh: function (frm) {
		frm.set_query('type', 'items', function () {
			return {
				filters: {
					'name': ['in', ['Lab Test Template', 'Clinical Procedure Template', 'Therapy Type']],
				}
			};
		});
	},
});
